import json
import numpy as np


CHECKLIST_FILENAME = "Data_Readiness_Checklist.json"
WIDGET_WIDTH = '900px'
DESCRIPTION_STYLE = {'description_width': 'initial'}
PLACEHOLDER = 'Click to select option'

# helper functions for loading / saving checklist data     

def load_checklist():
    """
    Load the checklist from a JSON file.

    Returns:
        dict: The contents of the checklist file as a dictionary.
    """
    with open(CHECKLIST_FILENAME, "r") as file:
        return json.load(file)

def save_checklist(checklist):
    """
    Save the checklist to a JSON file.The JSON
    data is pretty-printed with an indentation of 4 spaces.

    Args:
        checklist (dict): The checklist data to be saved.
    """
    with open(CHECKLIST_FILENAME, "w") as file:
        json.dump(checklist, file, indent=4)

def update_values(checklist, updates):
    """
    Update the values in a checklist with the provided updates.
    This function takes a checklist and a set of updates, and applies the updates to the checklist.
    If a section in the updates exists in the checklist, it updates the corresponding keys and values.
    If a section in the updates does not exist in the checklist, it adds the entire section to the checklist.

    Args:
        checklist (dict): The original checklist to be updated.
        updates (dict): A dictionary containing the updates to be applied. The structure should match that of the checklist.

    Returns:
        dict: The updated checklist.
    """
    for section, section_updates in updates.items():
        if section in checklist:
            for key, value in section_updates.items():
                checklist[section][key] = value
        else: 
            checklist[section] = section_updates
    return checklist
    
def update_checklist(b, updates):
    """
    Update the checklist with the provided updates and save it.
    This function loads the current checklist from a JSON file, applies the provided updates,
    and then saves the updated checklist back to the JSON file.

    Args:
        b: The button widget. 
        updates (dict): A dictionary containing the updates to be applied to the checklist.
    """
    checklist = load_checklist() # Open json file
    checklist = update_values(checklist, updates) # update the values in the Jupyter checklist
    save_checklist(checklist) # Save the updated checklist to JSON fil


def reset_checklist():
    with open('Data_Readiness_Checklist_blank.json', 'r') as blank_file:
        data = json.load(blank_file)

    with open('Data_Readiness_Checklist.json', 'w') as user_file:
        json.dump(data, user_file, indent=4)



# =========================================================
#            GRIDDED CHECKLIST HELPER FUNCTIONS           
# =========================================================


def find_general_info(dataset):
    try:
        # Read the information from the dataset. 
        title = dataset.attrs["title"]
        version = dataset.attrs["version"]

    except KeyError:
        print("Dict key not found")
    except ValueError:
        print("Value not accessible")
        
    # Print the information
    print("Dataset Name:", title)
    print("Dataset Version:", version)

    return {"DatasetName" : title, "DatasetVersion" : version}




def find_unit_data(dataset):

    # Store variable data
    variable_data = []
    
    for var_name in dataset.variables:
        variable = dataset.variables[var_name]  # Access the variable

        # Add the variable's information to the list
        if 'units' in dataset[var_name].attrs:
            variable_data.append({
                "variable": var_name,
                "datatype": str(dataset[var_name].dtype),
                    "unit": dataset[var_name].units
            })
        else:
            variable_data.append({
                "variable": var_name,
                "datatype": str(dataset[var_name].dtype),
                    "unit": "Unknown"
            })
            
    return variable_data



def find_total_data_volume(dataset):
    
    # Get the total size of the dataset in memory (bytes)
    total_size_bytes = dataset.nbytes
    
    # Convert to MB
    total_size_mb = total_size_bytes / (1024 ** 2)
    
    return total_size_mb


def find_dimensions(dataset):

    # Create a dict to store information
    dimensions_info = {}

    # Number of dimensions
    dimensions_info["num_dimensions"] = len(dataset.dims)

    # Create a dict to store the details of each dimension.
    dimensions_info["dimensions"] = {}

    # Create a variable to add datapoints to. 
    total_datapoints = 1

    # Inspect all dimensions
    for dim_name, dim_size in dataset.dims.items():
        # Add the dimension name and size to the dict.
        dimensions_info["dimensions"][dim_name] = dim_size

        # Calculate the total datapoints but exclude bands dims. 
        if 'bound' not in dim_name and 'bnd' not in dim_name:
            total_datapoints *= dim_size

    # Add the total datapoints to the dimensions_info dict
    dimensions_info["total_datapoints"] = total_datapoints
    
    return dimensions_info


def dimension_and_variable_names(dataset):
    
    # Store dims and variable data
    dimension_names = []
    variable_names = []
    
    # Print dimensions (names and sizes)
    for dim_name, dim in dataset.dims.items():
        dimension_names.append(dim_name)
    
    # Print variables (short and long names)
    for var_name, var in dataset.variables.items():
        variable = dataset.variables[var_name]
    
        if 'long_name' in dataset[var_name].attrs:
            variable_names.append({
                "variable" : var_name,
                "long_name" : dataset[var_name].long_name
            })
    
        else: 
            variable_names.append({
                "variable" : var_name,
                "long_name" : "N/A"
            })
            
    return dimension_names, variable_names


def find_missing_values(dataset):
    # Create a list to store results
    variable_stats = []
    
    # Iterate through all variables
    for var_name, data_array in dataset.data_vars.items():
        # Exclude variables with "bnd" or "bound" in their names
        if "bnd" in var_name.lower() or "bound" in var_name.lower():
            continue
    
        # Total number of values in the variable
        total_values = data_array.size
    
        # Null values (NaN) statistics
        missing_values_count = data_array.isnull().sum().item()
        percentage_missing = (missing_values_count / total_values) * 100
    
        # _FillValue statistics
        fill_value = data_array.attrs.get('_FillValue', None)
        if fill_value is not None:
            filled_values_count = (data_array == fill_value).sum().item()
            percentage_filled = (filled_values_count / total_values) * 100
        else:
            filled_values_count = 0
            percentage_filled = 0.0
    
        # Create a dictionary with statistics for the current variable
        stats = {
            "variable_name": var_name,
            "missing_values_count": missing_values_count,
            "percentage_missing": percentage_missing,
            "has_fill_value": fill_value is not None,
            "fill_value": fill_value,
            "filled_values_count": filled_values_count,
            "percentage_filled": percentage_filled,
        }
    
        # Add the stats dictionary to the results list
        variable_stats.append(stats)

        return variable_stats



def count_z_score_outliers_for_dataset(dataset, threshold=3):
    """
    Count Z-score outliers for each variable in a dataset, excluding variables with "bnd" or "bound" in their names.

    Parameters:
    - dataset (xarray.Dataset): The dataset to analyze.
    - threshold (float): The Z-score threshold for identifying outliers.

    Returns:
    - list: A list of dictionaries with statistics for each variable.
    """
    results = []
    
    # Loop through variables in the dataset
    for var_name, data_array in dataset.data_vars.items():
        # Skip variables with "bnd" or "bound" in their names
        if "bnd" in var_name.lower() or "bound" in var_name.lower():
            continue
        
        # Flatten the data and remove NaN values
        data_flat = data_array.values.flatten()
        data_clean = data_flat[~np.isnan(data_flat)]
        
        if len(data_clean) == 0:
            # Skip variables with no valid data
            continue
        
        # Calculate mean and standard deviation
        mean = np.mean(data_clean)
        std_dev = np.std(data_clean)
        
        # Compute Z-scores
        z_scores = (data_clean - mean) / std_dev
        
        # Identify outliers
        outliers = np.abs(z_scores) > threshold
        num_outliers = np.sum(outliers)
        total_values = len(data_clean)
        percentage_outliers = (num_outliers / total_values) * 100
        
        # Add statistics to the results
        results.append({
            "variable_name": var_name,
            "total_values": total_values,
            "num_outliers": num_outliers,
            "percentage_outliers": percentage_outliers,
        })
    
    return results

  



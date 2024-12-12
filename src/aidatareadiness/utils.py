import json


CHECKLIST_FILENAME = "Data_Readiness_Checklist.json"
widget_width = '900px'
description_style = {'description_width': 'initial'}
placeholder = 'Click to select option'

# Helper functions.

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
      
    print("=" * 75)
    print("{:<25}{:<25}{:25}".format("VARIABLE", "DATATYPE", "UNIT"))
    print("=" * 75)
    
    for variable in variable_data:
        print("{:<25}{:<25}{:25}".format(variable["variable"], variable["datatype"], variable["unit"]))
    
    return variable_data




  
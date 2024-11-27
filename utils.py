import json
import os
import pandas as pd
from scipy.stats import zscore
import matplotlib.pyplot as plt


CHECKLIST_FILENAME = "Data_Readiness_Checklist.json"
widget_width = '900px'
description_style = {'description_width': 'initial'}
placeholder = 'Click to select option'


# ================================================================
#      HELPER FUNCTIONS FOR LOADING / SAVING CHECKLIST DATA     
# ================================================================

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
#            TABULAR CHECKLIST HELPER FUNCTIONS           
# =========================================================

def read_file(file_path, **kwargs):
    """
    Reads a file into a pandas DataFrame based on its extension.
    
    Parameters:
        file_path (str): The path to the file.
        **kwargs: Additional keyword arguments to pass to pandas reading functions.
        
    Returns:
        pd.DataFrame: The data from the file as a DataFrame.
    
    Raises:
        ValueError: If the file extension is unsupported or the file does not exist.

    Example usage:
        df = read_file("data.csv")
        df_txt = read_file("data.txt", delimiter=',')  # Custom delimiter for txt
        df_excel = read_file("data.xlsx", sheet_name="Sheet1")
    """

    # Check if the file exists
    if not os.path.exists(file_path, **kwargs):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Get the file extension
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    # Load different file types
    if file_extension == ".csv":
        return pd.read_csv(file_path, **kwargs)
    elif file_extension in [".txt", ".tsv"]:
        return pd.read_csv(file_path, delimiter="\t", **kwargs)
    elif file_extension in [".xls", ".xlsx"]:
        return pd.read_excel(file_path, **kwargs)
    elif file_extension == ".json":
        return pd.read_json(file_path, **kwargs)
    elif file_extension == ".parquet":
        return pd.read_parquet(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")



def check_spatial_coverage(df, lat_column, lon_column, expected_bounds):
    """
    Checks the spatial coverage of a dataset against the expected geographic bounds.
    
    Parameters:
        df (pd.DataFrame): The dataset as a pandas DataFrame.
        lat_column (str): Name of the column containing latitude values.
        lon_column (str): Name of the column containing longitude values.
        expected_bounds (dict): Dictionary specifying the expected bounds with keys:
            - "min_lat": Minimum latitude
            - "max_lat": Maximum latitude
            - "min_lon": Minimum longitude
            - "max_lon": Maximum longitude
    
    Returns:
        dict: A dictionary containing the results of the analysis.
    """
    # Ensure latitude and longitude columns are numeric
    if not pd.api.types.is_numeric_dtype(df[lat_column]):
        raise ValueError(f"The column {lat_column} must contain numeric values.")
    if not pd.api.types.is_numeric_dtype(df[lon_column]):
        raise ValueError(f"The column {lon_column} must contain numeric values.")

    # Actual bounds
    actual_bounds = {
        "min_lat": float(df[lat_column].min()),
        "max_lat": float(df[lat_column].max()),
        "min_lon": float(df[lon_column].min()),
        "max_lon": float(df[lon_column].max())
    }

    # Check if all points are within the expected bounds
    within_bounds = (
        (df[lat_column] >= expected_bounds["min_lat"]) &
        (df[lat_column] <= expected_bounds["max_lat"]) &
        (df[lon_column] >= expected_bounds["min_lon"]) &
        (df[lon_column] <= expected_bounds["max_lon"])
    )
    out_of_bounds_points = df[~within_bounds]

    # Results
    coverage_results = {
        "expected_bounds": expected_bounds,
        "actual_bounds": actual_bounds,
        "all_within_bounds": out_of_bounds_points.empty,
        "out_of_bounds_points": out_of_bounds_points
    }

    print("Expected Bounds:", coverage_results["expected_bounds"])
    print("Actual Bounds:", coverage_results["actual_bounds"])
    print("All Points Within Bounds:", coverage_results["all_within_bounds"])
    if not coverage_results["all_within_bounds"]:
        print("Out of Bounds Points:")
        print(coverage_results["out_of_bounds_points"])

    return coverage_results


def check_temporal_coverage(df, date_column, expected_start, expected_end):
    """
    Checks and prints the temporal coverage of a dataset against the expected range.
    
    Parameters:
        df (pd.DataFrame): The dataset as a pandas DataFrame.
        date_column (str): Name of the column containing the dates.
        expected_start (str): Expected start date (e.g., "2020-01-01").
        expected_end (str): Expected end date (e.g., "2023-12-31").
    
    Returns:
        dict: A dictionary containing the results of the analysis.
    """
    # Ensure the date column is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])

    # Ensure the date column is sorted
    df = df.sort_values(by=date_column)

    time_format = "%Y-%m-%d"

    # Actual coverage
    actual_start = df[date_column].min()
    actual_end = df[date_column].max()

    # Create a date range for expected coverage
    expected_dates = pd.date_range(start=expected_start, end=expected_end)

    # Check for missing dates
    actual_dates = pd.to_datetime(df[date_column].drop_duplicates())
    missing_dates = expected_dates.difference(actual_dates).strftime(time_format)

    # Results
    coverage_results = {
        "expected_start": expected_start,
        "expected_end": expected_end,
        "actual_start": actual_start.strftime(time_format),
        "actual_end": actual_end.strftime(time_format),
        "missing_dates": missing_dates.tolist(),
        "num_missing_dates" : len(missing_dates)
    }

    print("Expected Start:", coverage_results["expected_start"])
    print("Actual Start:", coverage_results["actual_start"])
    print("Expected End:", coverage_results["expected_end"])
    print("Actual End:", coverage_results["actual_end"])
    print("Number of Missing Dates:", coverage_results["num_missing_dates"])
    print("Missing Dates:", coverage_results["missing_dates"])

    return coverage_results


def csv_size_file_info(df, file_path):
    """
    Prints and returns information about a tabular (csv) file:
    - Number of rows
    - Data dimensions
    - Total memory used
    
    Args:
    df (pd.DataFrame): The DataFrame you are working with.
    file_path (str): The path to the file.
    
    Returns:
    dict: A dictionary containing the file information.
    """
    
    # Get file information
    num_rows = len(df)
    data_dimensions = df.shape
    
    df_memory_used = df.memory_usage(deep=True).sum()
    df_memory_used = (
        f"{df_memory_used / 1024:.2f} KB"
        if df_memory_used < 1024**2
        else f"{df_memory_used / 1024**2:.2f} MB"
    )
    
    file_size = os.path.getsize(file_path)
    file_size = (
        f"{file_size / 1024:.2f} KB"
        if file_size < 1024**2
        else f"{file_size / 1024**2:.2f} MB"
    )
    

    file_results = {
        "Number of rows": num_rows,
        "Data dimensions": len(data_dimensions),
        "Data dimensions detail": data_dimensions,
        "DataFrame memory used": df_memory_used,
        "File memory used": file_size
    }
    
    # Print the information
    print(f"Number of rows: {file_results["Number of rows"]}")
    print(f"Data dimensions: {file_results["Data dimensions"]}")
    print(f"Data dimensions detail (rows, columns): {file_results["Data dimensions detail"]}")
    print(f"DataFrame memory used: {file_results["DataFrame memory used"]}")
    print(f"File memory used: {file_results["File memory used"]}")
    
    # Return the information as a dictionary
    return file_results



def null_percent(df):
    """
    Returns a new pandas DataFrame of the count and percentage of null values 
    in each column of a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame for which to calculate and 
    print the count and percentage of missing values.

    Returns:
    df (pd.DataFrame): A new DataFrame with the count and percentage of null values.
    
    """
    missing_count = df.isna().sum()
    missing_percentage = missing_count / len(df) * 100
    formatted_percentage = missing_percentage.apply(lambda x: f"{x:.1f}%")

   # Create a new DataFrame with both counts and formatted percentages
    result_df = pd.DataFrame({
        'Count': missing_count,
        'Percent': formatted_percentage
    })
    
    # print("PERCENTAGE OF NULL VALUES\n")
    # print(result_df)

    return result_df



def mask_values(df, values_to_mask, new_value):
    """
    Masks specified values in a DataFrame and replaces them with a specified value.

    Parameters:
    df (pd.DataFrame): The DataFrame in which to mask the specified values.
    values_to_mask: An array of values to replace.
    new_value: The new value you wish to replace the values with in values_to_mask.

    Returns:
    pd.DataFrame: A new DataFrame with the specified values replaced with a new value.
    """
    df_masked = df.mask(df.isin(values_to_mask), new_value)
    
    return df_masked


def plot_violin_graphs(dataframe, column_feature_names):
    """
    Creates violin plots for columns using only Matplotlib.
    Arguments - a Pandas DataFrame and a list of DataFrame column names.
    """
    
    fig, axes = plt.subplots(nrows=1, ncols=len(column_feature_names), figsize=(18, 5))

    for i, column in enumerate(column_feature_names):
        # Get the data for the current column
        data = dataframe[column]

        # Create the violin plot on the respective axis
        parts = axes[i].violinplot(data, showmeans=False, showmedians=True)
        
        # Remove x-axis labels and ticks
        axes[i].set_xticks([])

        # Title the plot
        axes[i].set_title(column)


    plt.tight_layout()    
    plt.show()


def print_z_scores(df):
    """
    Calculate and display z-scores in a pie chart.
    Returns the total z_scores and those over 2 and 3.

    This function computes the z-scores for each column in the provided DataFrame,
    counts how many of these z-scores are greater than 2 and 3 in absolute value,
    and visualises the results as a pie chart.

    Parameters:
    df (pd.DataFrame): A pandas DataFrame containing numerical data for which z-scores 
                       will be calculated.
    Returns:
    Total number of Z-Scores
    Z-Scores > 2
    Z-Scores > 3
    """
    z_scores = df.apply(zscore)
    abs_z_scores = abs(z_scores)
    num_z_scores = len(z_scores)
    high_z_scores_2 = (abs_z_scores > 2).sum().sum()
    high_z_scores_3 = (abs_z_scores > 3).sum().sum()
    
    # print('Number of values with a z-score greater than 2:', high_z_scores_2)
    # print('Number of values with a z-score greater than 3:', high_z_scores_3)
    # print('Total z_scores:', len(z_scores))

    # Prepare data for the pie chart
    labels = [f'{num_z_scores} - Total', f'{high_z_scores_2} - Z-Score > 2', f'{high_z_scores_3} - Z-Score > 3']
    sizes = [num_z_scores, high_z_scores_2, high_z_scores_3]
    
    # Plot the pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=0)
    plt.title('Pie Chart of Z-Scores and High Z-Scores')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Show the pie chart
    plt.show()

    # Return the counts
    return num_z_scores, high_z_scores_2, high_z_scores_3



# =========================================================
#            GRIDDED CHECKLIST HELPER FUNCTIONS           
# =========================================================








  
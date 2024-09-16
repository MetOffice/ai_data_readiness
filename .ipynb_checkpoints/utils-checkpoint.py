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



def print_json_info(b):
    """
    Loads a copy of the json file to checklist variable. 
    Then prints the json file contents to Jupyter notebook cell output.

    Arguments: b - represents the button calling the function. 
    """
    
    checklist = load_checklist()
    with output:
        clear_output()
        for key, value in checklist.items():
            print(f"{key}:")
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"  {value}")

  
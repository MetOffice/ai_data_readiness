import json


CHECKLIST_FILENAME = "Data_Readiness_Checklist.json"

# Helper functions.

def load_checklist():
    with open(CHECKLIST_FILENAME, "r") as file:
        return json.load(file)

def save_checklist(checklist):
    with open(CHECKLIST_FILENAME, "w") as file:
        json.dump(checklist, file, indent=4)

def update_values(checklist, updates):
    for section, section_updates in updates.items():
        if section in checklist:
            for key, value in section_updates.items():
                checklist[section][key] = value
        else: 
            checklist[section] = section_updates
    return checklist
    
def update_checklist(b, updates):
    checklist = load_checklist() # Open json file
    checklist = update_values(checklist, updates) # update the values in the Jupyter checklist
    save_checklist(checklist) # Save the updated checklist to JSON fil
  
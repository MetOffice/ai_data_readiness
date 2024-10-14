"""
A script to download the first HadCRUT5 Analysis Anomalies ensemble file. 
This process will download the first 10 ensemble files as a zip, extract and save the first file then delete the zip to conserve memory.
"""
import os
import requests
import zipfile

url = "https://www.metoffice.gov.uk/hadobs/hadcrut5/data/HadCRUT.5.0.2.0/analysis/HadCRUT.5.0.2.0.analysis.anomalies.ensemble_mean.nc"
response = requests.get(url)
print("Downloading data")

if not os.path.exists("data"):      
    os.makedirs("data")
    print("Creating data folder")
	
with open("data/HadCRUT.5.0.2.0.analysis.anomalies.ensemble_mean.nc", "wb") as file:
	file.write(response.content)
	print("File saved to data folder")

# with zipfile.ZipFile("HadCRUT5_data.zip", "r") as zip_ref:
#     file_list = zip_ref.namelist()
#     first_file = file_list[0]
#     zip_ref.extract(first_file, "data")
#     print("Extracting first file")
    
#     os.rename(os.path.join("data", first_file), os.path.join("data", os.path.basename(first_file)))
#     print("Data added to data/ folder")
        
# # Path to the zip file
# zip_file_path = "HadCRUT5_data.zip"

# # Check if the file exists before attempting to delete it
# print("Cleaning up")
# if os.path.exists(zip_file_path):
#     os.remove(zip_file_path)
#     print("Zip file has been deleted.")


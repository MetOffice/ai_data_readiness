# (C) British Crown Copyright 2017-2025, Met Office.
# Please see LICENSE.md for license details.

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

if not os.path.exists("../data"):      
    os.makedirs("../data")
    print("Creating data folder")
	
with open("../data/HadCRUT.5.0.2.0.analysis.anomalies.ensemble_mean.nc", "wb") as file:
	file.write(response.content)
	print("File saved to data folder")

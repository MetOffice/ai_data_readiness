# (C) British Crown Copyright 2017-2025, Met Office.
# Please see LICENSE.md for license details.

import requests
import os
import argparse
from bs4 import BeautifulSoup

# Base URL for NOAA NCEI global-hourly data in 2024
BASE_URL = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/2020/"

# Directory where data will be downloaded
DOWNLOAD_DIR = "./data"

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_file(url, download_dir):
    local_filename = os.path.join(download_dir, url.split('/')[-1])
    print(f"Downloading {url} to {local_filename}")

    # Download the file with streaming to avoid loading large files into memory
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Will raise an exception for 404/500 errors
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    print(f"Downloaded: {local_filename}")

def get_station_ids(base_url):
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    station_ids = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.csv'):
            station_id = href.split('.')[0]
            station_ids.append(station_id)
    return station_ids

def download_noaa_data(base_url, download_dir, num_files):
    station_ids = get_station_ids(base_url)
    # Limit the number of station IDs to the specified number of files
    station_ids = station_ids[:num_files]
    
    # Loop through the station IDs and construct file URLs
    for station_id in station_ids:
        file_url = f"{base_url}{station_id}.csv"
        try:
            download_file(file_url, download_dir)
        except requests.exceptions.HTTPError as e:
            print(f"Failed to download {file_url}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download NOAA NCEI global-hourly data.")
    parser.add_argument('num_files', type=int, help="Number of files to download")
    args = parser.parse_args()

    # Run the download function with the specified number of files
    download_noaa_data(BASE_URL, DOWNLOAD_DIR, args.num_files)

    print("All files downloaded!")

if __name__ == "__main__":
    main()

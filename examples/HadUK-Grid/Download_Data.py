import requests
import os
import argparse
from bs4 import BeautifulSoup
from base64 import b64encode
import json

# Base URL for HadUK-Grid daily rainfall data
BASE_URL = "https://dap.ceda.ac.uk/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.3.0.ceda/60km/rainfall/day/latest/"

TOKEN_URL = "https://services-beta.ceda.ac.uk/api/token/create/"

# Directory where data will be downloaded
DOWNLOAD_DIR = "./data"

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_file(url, download_dir):
    local_filename = os.path.join(download_dir, url.split('/')[-1])
    print(f"Downloading {url} to {local_filename}")

    username = os.environ["CEDA_USERNAME"]
    password = os.environ["CEDA_PASSWORD"]

    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")

    headers = {
      "Authorization": f"Bearer {token}"
    }

    response = requests.request("POST", TOKEN_URL, headers=headers)

    # If successful, this will return a JSON response containing the token
    # Print the response for debugging
    print(response.text)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = json.loads(response.text)
        token = response_data.get("access_token")
        if token:
            print(f"Token: {token}")
        else:
            print("Error: 'access_token' not found in the response.")
            return
    else:
        print(f"Error: Received status code {response.status_code}")
        return

    # Download the file with streaming to avoid loading large files into memory
    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()  # Will raise an exception for 404/500 errors
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    print(f"Downloaded: {local_filename}")

def get_nc_files(base_url):
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    nc_files = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.nc'):
            nc_files.append(href)
    return nc_files

def download_haduk_data(base_url, download_dir, num_files):
    nc_files = get_nc_files(base_url)
    
    # Sort files by name to get the most recent ones (assuming the file names are in chronological order)
    nc_files.sort(reverse=True)
    
    # Limit the number of files to the specified number
    nc_files = nc_files[:num_files]
    
    # Loop through the file URLs and download them
    for nc_file in nc_files:
        file_url = f"{base_url}{nc_file}"
        try:
            download_file(file_url, download_dir)
        except requests.exceptions.HTTPError as e:
            print(f"Failed to download {file_url}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download HadUK-Grid daily rainfall data.")
    parser.add_argument('num_files', type=int, help="Number of files to download")
    args = parser.parse_args()

    # Run the download function with the specified number of files
    download_haduk_data(BASE_URL, DOWNLOAD_DIR, args.num_files)


    print("All files downloaded!")

if __name__ == "__main__":
    main()

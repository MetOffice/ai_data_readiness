import requests
import os
import argparse
from bs4 import BeautifulSoup

# Base URL for HadUK-Grid daily rainfall data
BASE_URL = "https://dap.ceda.ac.uk/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.3.0.ceda/25km/tas/mon/latest/"

# Directory where data will be downloaded


def download_file(url, download_dir):
    local_filename = os.path.join(download_dir, url.split('/')[-1])
    print(f"Downloading {url} to {local_filename}")
    
    try:
        token = os.environ["CEDA_TOKEN"]
    except Exception as e:
        raise e

    headers = {
      "Authorization": f"Bearer {token}"
    }

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
        if href and (href.endswith('.nc')):
            nc_files.append(href)
    return nc_files

def download_haduk_data(base_url, download_dir, num_files, raise_failed_download):

    # Ensure download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    nc_files = get_nc_files(base_url)

    if nc_files == []:
        raise Exception(".nc files not found at URL")
    
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
            if raise_failed_download == True:
                raise e
            else:
                print(f"Failed to download {file_url}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download HadUK-Grid daily rainfall data.")
    parser.add_argument('--num_files', '-n', type=int, help="Number of files to download", default=2, required=False)
    parser.add_argument('--dir', '-d', type=str, help="Directory to download the data into", default="./data", required=False)
    parser.add_argument('--raise_failed_download', '-r', type=bool, help="Raise exception if download fails", default=False, required=False)
    args = parser.parse_args()

    # Run the download function with the specified number of files
    download_haduk_data(BASE_URL, args.dir, args.num_files, args.raise_failed_download)

if __name__ == "__main__":
    main()

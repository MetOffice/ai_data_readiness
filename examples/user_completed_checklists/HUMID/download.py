import requests
import sys, os
import argparse
from urllib.request import build_opener
from datetime import datetime, date, timedelta
import xarray as xr

# Base URL for NCAR HUMID daily data
BASE_URL = 'https://data.rda.ucar.edu/d314008/'
 
# opener
opener = build_opener()
 
 
def download_humid_data(base_url, start_datestring, end_datestring, download_dir, raise_failed_download):
 
    # Ensure download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
 
    start_date = datetime.strptime(start_datestring, '%m-%d-%Y').date()
    end_date = datetime.strptime(end_datestring, '%m-%d-%Y').date()
    delta = timedelta(days=1)
    date = start_date
    filelist = []
    while date <= end_date:
        filelist.append(f'{base_url}{date.year}{date.month:02d}/conus_HUMID_{date.year}{date.month:02d}{date.day:02d}.nc4')
        date += delta
 
    if filelist == []:
        raise Exception("files not found at URL")
 
    for file in filelist:
        ofile = os.path.basename(file)
        sys.stdout.write("downloading " + ofile + " ... ")
        sys.stdout.flush()
        infile = opener.open(file)
        outfile = open(f'{download_dir}/{ofile}', "wb")
        outfile.write(infile.read())
        outfile.close()
        sys.stdout.write("done\n")

        dataset = xr.open_dataset(f'{download_dir}/{ofile}')
        lat_imin = 1498
        lat_imax = 1754
        lon_imin = 1502
        lon_imax = 1758
        var_list = ['FRC_URB2D', 'URB_CAT', 'q2', 't2_raw', 'tb_urb2d', 'tb_urb2d_max']
        sliced_var = dataset[var_list].isel(lat=slice(lat_imin, lat_imax), lon=slice(lon_imin, lon_imax))
        sliced_var.to_netcdf(f'{download_dir}/proc_{ofile}')
        os.remove(f'{download_dir}/{ofile}')
 
 
def main():
    parser = argparse.ArgumentParser(description='Download HUMID daily data.')
    parser.add_argument('--start_date', '-s', type=str, help='Start date, form mm-dd-YYYY', default='01-01-2018', required=False)
    parser.add_argument('--end_date', '-e', type=str, help='End date, form mm-dd-YYYY', default='01-31-2018', required=False)
    parser.add_argument('--dir', '-d', type=str, help="Directory to download the data into", default='./data', required=False)
    parser.add_argument('--raise_failed_download', '-r', type=bool, help="Raise exception if download fails", default=False, required=False)
    args = parser.parse_args()
 
    # Run the download function with the specified number of files
    download_humid_data(BASE_URL, args.start_date, args.end_date, args.dir, args.raise_failed_download)
 
 
if __name__ == "__main__":
    main()

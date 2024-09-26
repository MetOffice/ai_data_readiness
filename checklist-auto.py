import os
from tkinter import Tk, filedialog
import xarray as xr
import numpy as np
import os

def select_file():
    """Open a file dialog to select a file."""
    root = Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(title="Select a weather and climate data file")
    return file_path

def detect_gridded_format_and_open(file_path):
    # Detect the file format based on the file extension
    _, file_extension = os.path.splitext(file_path)
    
    # Define a dictionary to map file extensions to xarray engines
    format_engine_map = {
        # NetCDF
        '.nc': 'netcdf4',  
        # GRIB
        '.grib': 'cfgrib',  
        # HDF5
        '.h5': 'h5netcdf',  
        '.hdf5': 'h5netcdf',  
        # GeoTIFF
        '.tif': 'rasterio',  
        '.tiff': 'rasterio',  
        # Zarr
        '.zarr': 'zarr',  
    }
    
    # Check if the file format is supported
    if file_extension in format_engine_map:
        engine = format_engine_map[file_extension]
        try:
            # Open the file using xarray with the appropriate engine
            ds = xr.open_dataset(file_path, engine=engine)
            print(f"Successfully opened {file_path} with engine {engine}")
            return ds
        except Exception as e:
            print(f"Failed to open {file_path} with engine {engine}: {e}")
            return None
    else:
        print(f"Unsupported file format: {file_extension}")
        return None

def get_spatial_resolution_and_coverage(dataset):
    # Assuming the dataset has latitude and longitude coordinates
    if 'latitude' in dataset.coords and 'longitude' in dataset.coords:
        lat = dataset['latitude']
        lon = dataset['longitude']
    elif 'lat' in dataset.coords and 'lon' in dataset.coords:
        lat = dataset['lat']
        lon = dataset['lon']
    else:
        print("Latitude and Longitude coordinates not found in the dataset.")
        return None, None
    
    # Calculate resolution (assuming uniform grid)
    lat_res = np.abs(lat[1] - lat[0]).values if lat.size > 1 else None
    lon_res = np.abs(lon[1] - lon[0]).values if lon.size > 1 else None
    
    # Calculate coverage
    lat_min, lat_max = lat.min().values, lat.max().values
    lon_min, lon_max = lon.min().values, lon.max().values
    
    resolution = (lat_res, lon_res)
    coverage = {
        'latitude': (lat_min, lat_max),
        'longitude': (lon_min, lon_max)
    }
    
    return resolution, coverage

def get_temporal_resolution_and_coverage(dataset):
    # Assuming the dataset has a time coordinate
    if 'time' in dataset.coords:
        time = dataset['time']
    else:
        print("Time coordinate not found in the dataset.")
        return None, None
    
    # Calculate temporal resolution (assuming uniform time steps)
    if time.size > 1:
        time_res = np.diff(time.values).astype('timedelta64[h]').astype(int)[0]  # Resolution in hours
    else:
        time_res = None
    
    # Calculate temporal coverage
    time_min, time_max = time.min().values, time.max().values
    
    resolution = time_res
    coverage = {
        'time': (time_min, time_max)
    }
    
    return resolution, coverage

def check_spatial_consistency(dataset):
    # Check spatial consistency
    if 'latitude' in dataset.coords and 'longitude' in dataset.coords:
        lat = dataset['latitude']
        lon = dataset['longitude']
    elif 'lat' in dataset.coords and 'lon' in dataset.coords:
        lat = dataset['lat']
        lon = dataset['lon']
    else:
        # Latitude and Longitude coordinates not found in the dataset.")
        return None 
    
    lat_diff = np.diff(lat.values)
    lon_diff = np.diff(lon.values)

    if not np.allclose(lat_diff, lat_diff[0]) or not np.allclose(lon_diff, lon_diff[0]):
        print("Spatial resolution is not consistent.")
        return False

    return True
    

def check_temporal_consistency(dataset):
    # Check temporal consistency
    if 'time' in dataset.coords:
        time = dataset['time']
    else:
        # Time coordinate not found in the dataset
        return None
    
    time_diff = np.diff(time.values).astype('timedelta64[h]').astype(int)
    
    if not np.allclose(time_diff, time_diff[0]):
        # Temporal resolution is not consistent
        return False 
    
    # Spatial and temporal resolutions are consistent
    return True 

def main():
    file_path = select_file()
    if not file_path:
        print("No file selected.")
        return
    
    dataset = detect_gridded_format_and_open(file_path)

    if dataset is not None:
        spatial_resolution, spatial_coverage = get_spatial_resolution_and_coverage(dataset)
        temporal_resolution, temporal_coverage = get_temporal_resolution_and_coverage(dataset)        
        if spatial_resolution and spatial_coverage:
            print(f"Resolution: Latitude - {spatial_resolution[0]} degrees, Longitude - {spatial_resolution[1]} degrees")
            print(f"Coverage: Latitude - {spatial_coverage['latitude'][0]} to {spatial_coverage['latitude'][1]} degrees, "
                f"Longitude - {spatial_coverage['longitude'][0]} to {spatial_coverage['longitude'][1]} degrees")

        if temporal_resolution and temporal_coverage:
            print(f"Temporal Resolution: {temporal_resolution} hours")
            print(f"Temporal Coverage: {temporal_coverage['time'][0]} to {temporal_coverage['time'][1]}")

        spatial_consistency = check_spatial_consistency(dataset)
        temporal_consistency = check_temporal_consistency(dataset)

        if spatial_consistency != None:
            print(f"Spatial Consistency: {spatial_consistency}")
        if temporal_consistency != None:
            print(f"Temporal Consistency: {temporal_consistency}")

if __name__ == "__main__":
    main()

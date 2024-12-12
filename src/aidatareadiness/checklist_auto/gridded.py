import os
import logging
import argparse
import xarray as xr
import numpy as np
import json
import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = ['.nc', '.grib', '.h5', '.hdf5', '.tif', '.tiff', '.zarr']

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process and analyze gridded climate data.")
    
    parser.add_argument('--files', nargs='*', help="List of paths to weather and climate data files")
    parser.add_argument('--dirs', nargs='*', help="List of directories containing weather and climate data files")
    parser.add_argument('--output', type=str, help="Path to save the analysis results in CSV or JSON format")
    
    args = parser.parse_args()
    
    if not args.files and not args.dirs:
        parser.error("Either --files or --dirs must be specified.")
    
    return args

def detect_gridded_format_and_open(file_path):
    """Detect the file format based on the file extension and open it with xarray."""
    _, file_extension = os.path.splitext(file_path)
    
    format_engine_map = {
        '.nc': 'netcdf4',  # NetCDF
        '.grib': 'cfgrib',  # GRIB
        '.h5': 'h5netcdf',  # HDF5
        '.hdf5': 'h5netcdf',
        '.tif': 'rasterio',  # GeoTIFF
        '.tiff': 'rasterio',
        '.zarr': 'zarr',  # Zarr
    }
    
    if file_extension not in format_engine_map:
        logger.error(f"Unsupported file format: {file_extension} for {file_path}")
        return None
    
    engine = format_engine_map[file_extension]
    try:
        ds = xr.open_dataset(file_path, engine=engine)
        logger.info(f"Successfully opened {file_path} with engine {engine}")
        return ds
    except ValueError as e:
        logger.error(f"Value error when opening {file_path} with engine {engine}: {e}")
    except IOError as e:
        logger.error(f"IO error when opening {file_path}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error when opening {file_path}: {e}")
    
    return None

def get_spatial_resolution_and_coverage(dataset):
    """Calculate the spatial resolution and coverage of the dataset."""
    lat_keys = ['latitude', 'lat']
    lon_keys = ['longitude', 'lon']
    
    lat = next((dataset.coords[k] for k in lat_keys if k in dataset.coords), None)
    lon = next((dataset.coords[k] for k in lon_keys if k in dataset.coords), None)
    
    if lat is None or lon is None:
        logger.warning("Latitude and/or Longitude coordinates not found in the dataset.")
        return None, None
    
    lat_res = np.abs(lat[1] - lat[0]).values if lat.size > 1 else None
    lon_res = np.abs(lon[1] - lon[0]).values if lon.size > 1 else None
    
    lat_min, lat_max = lat.min().values, lat.max().values
    lon_min, lon_max = lon.min().values, lon.max().values
    
    resolution = (lat_res, lon_res)
    coverage = {
        'latitude': (lat_min, lat_max),
        'longitude': (lon_min, lon_max)
    }
    
    logger.info(f"Spatial Resolution: Latitude - {lat_res}, Longitude - {lon_res}")
    logger.info(f"Spatial Coverage: Latitude from {lat_min} to {lat_max}, Longitude from {lon_min} to {lon_max}")
    
    return resolution, coverage

def get_temporal_resolution_and_coverage(dataset):
    """Calculate the temporal resolution and coverage of the dataset."""
    if 'time' in dataset.coords:
        time = dataset['time']
    else:
        logger.warning("Time coordinate not found in the dataset.")
        return None, None
    
    if time.size > 1:
        time_res = np.diff(time.values).astype('timedelta64[h]').mean().astype(int)
    else:
        time_res = None
    
    time_min, time_max = time.min().values, time.max().values
    
    logger.info(f"Temporal Resolution: {time_res} hours")
    logger.info(f"Temporal Coverage: From {time_min} to {time_max}")
    
    return time_res, {
        'time': (time_min, time_max)
    }

def check_spatial_consistency(dataset):
    """Check if the spatial resolution is consistent across the dataset."""
    lat_keys = ['latitude', 'lat']
    lon_keys = ['longitude', 'lon']
    
    lat = next((dataset.coords[k] for k in lat_keys if k in dataset.coords), None)
    lon = next((dataset.coords[k] for k in lon_keys if k in dataset.coords), None)
    
    if lat is None or lon is None:
        logger.warning("Latitude and/or Longitude coordinates not found in the dataset.")
        return None
    
    lat_diff = np.diff(lat.values)
    lon_diff = np.diff(lon.values)

    if not np.allclose(lat_diff, lat_diff[0]) or not np.allclose(lon_diff, lon_diff[0]):
        logger.warning("Spatial resolution is not consistent.")
        return False

    logger.info("Spatial resolution is consistent.")
    return True

def check_temporal_consistency(dataset):
    """Check if the temporal resolution is consistent across the dataset."""
    if 'time' in dataset.coords:
        time = dataset['time']
    else:
        logger.warning("Time coordinate not found in the dataset.")
        return None
    
    time_diff = np.diff(time.values).astype('timedelta64[h]').astype(int)
    
    if not np.allclose(time_diff, time_diff[0]):
        logger.warning("Temporal resolution is not consistent.")
        return False

    logger.info("Temporal resolution is consistent.")
    return True

def save_results(results, output_path):
    """Save the results in the specified format (JSON or CSV)."""
    if output_path.endswith(".json"):
        with open(output_path, "w") as f:
            json.dump(results, f)
    elif output_path.endswith(".csv"):
        df = pd.DataFrame([results])
        df.to_csv(output_path, index=False)
    else:
        logger.error(f"Unsupported output format for {output_path}")

def process_file(file_path, output_path=None):
    """Process a single file."""
    dataset = detect_gridded_format_and_open(file_path)

    if dataset is not None:
        resolution, coverage = get_spatial_resolution_and_coverage(dataset)
        temporal_resolution, temporal_coverage = get_temporal_resolution_and_coverage(dataset)
        
        spatial_consistency = check_spatial_consistency(dataset)
        temporal_consistency = check_temporal_consistency(dataset)
        
        result = {
            'file': file_path,
            'spatial_resolution': resolution,
            'spatial_coverage': coverage,
            'temporal_resolution': temporal_resolution,
            'temporal_coverage': temporal_coverage,
            'spatial_consistency': spatial_consistency,
            'temporal_consistency': temporal_consistency
        }
        
        if output_path:
            save_results(result, output_path)
        
        # Close the dataset to free resources
        dataset.close()
        
        return result

def process_directory(directory, output_path=None):
    """Process all supported files in a directory sequentially."""
    all_files = []
    for root, _, files in os.walk(directory):
        all_files.extend([os.path.join(root, f) for f in files if os.path.splitext(f)[1] in SUPPORTED_FORMATS])
    
    results = []
    with tqdm(total=len(all_files), desc="Processing files") as pbar:
        for file_path in all_files:
            result = process_file(file_path, output_path)
            if result:
                results.append(result)
            pbar.update(1)

    return results

def main():
    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Parse the command-line arguments
    args = parse_arguments()

    # Process files
    results = []
    if args.files:
        for file_path in args.files:
            logger.info(f"Processing file: {file_path}")
            result = process_file(file_path, args.output)
            if result:
                results.append(result)
    
    # Process directories
    if args.dirs:
        for directory in args.dirs:
            logger.info(f"Processing directory: {directory}")
            dir_results = process_directory(directory, args.output)
            results.extend(dir_results)

    if args.output:
        save_results(results, args.output)
    else:
        logger.info(f"Processing completed. Results: {results}")

if __name__ == "__main__":
    main()

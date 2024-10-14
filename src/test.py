import os
import logging
import argparse
import xarray as xr
import numpy as np

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = ['.nc', '.grib', '.h5', '.hdf5', '.tif', '.tiff', '.zarr']

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process and analyze gridded climate data.")
    
    # Add arguments to accept either a file or a directory
    parser.add_argument('--file', type=str, help="Path to a weather and climate data file")
    parser.add_argument('--dir', type=str, help="Path to a directory containing weather and climate data files")
    
    # Ensure that one of the two is provided
    args = parser.parse_args()
    
    if not args.file and not args.dir:
        parser.error("Either --file or --dir must be specified.")
    
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
    
    if file_extension in format_engine_map:
        engine = format_engine_map[file_extension]
        try:
            ds = xr.open_dataset(file_path, engine=engine)
            logger.info(f"Successfully opened {file_path} with engine {engine}")
            return ds
        except Exception as e:
            logger.error(f"Failed to open {file_path} with engine {engine}: {e}")
            return None
    else:
        logger.error(f"Unsupported file format: {file_extension}")
        return None

def get_spatial_resolution_and_coverage(dataset):
    """Calculate the spatial resolution and coverage of the dataset."""
    if 'latitude' in dataset.coords and 'longitude' in dataset.coords:
        lat = dataset['latitude']
        lon = dataset['longitude']
    elif 'lat' in dataset.coords and 'lon' in dataset.coords:
        lat = dataset['lat']
        lon = dataset['lon']
    else:
        logger.warning("Latitude and Longitude coordinates not found in the dataset.")
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
        time_res = np.diff(time.values).astype('timedelta64[h]').astype(int)[0]  # Resolution in hours
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
    if 'latitude' in dataset.coords and 'longitude' in dataset.coords:
        lat = dataset['latitude']
        lon = dataset['longitude']
    elif 'lat' in dataset.coords and 'lon' in dataset.coords:
        lat = dataset['lat']
        lon = dataset['lon']
    else:
        logger.warning("Latitude and Longitude coordinates not found in the dataset.")
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

def process_file(file_path):
    """Process a single file."""
    dataset = detect_gridded_format_and_open(file_path)

    if dataset is not None:
        resolution, coverage = get_spatial_resolution_and_coverage(dataset)
        temporal_resolution, temporal_coverage = get_temporal_resolution_and_coverage(dataset)
        
        if resolution and coverage:
            logger.info(f"Spatial Resolution: {resolution[0]} degrees (latitude), {resolution[1]} degrees (longitude)")
            logger.info(f"Spatial Coverage: Latitude from {coverage['latitude'][0]} to {coverage['latitude'][1]}, "
                        f"Longitude from {coverage['longitude'][0]} to {coverage['longitude'][1]}")
        
        if temporal_resolution and temporal_coverage:
            logger.info(f"Temporal Resolution: {temporal_resolution} hours")
            logger.info(f"Temporal Coverage: From {temporal_coverage['time'][0]} to {temporal_coverage['time'][1]}")
        
        spatial_consistency = check_spatial_consistency(dataset)
        temporal_consistency = check_temporal_consistency(dataset)
        
        if spatial_consistency is None:
            logger.error("Latitude and Longitude coordinates not found in the dataset.")
        else:
            logger.info(f"Spatial Consistency: {spatial_consistency}")
        
        if temporal_consistency is None:
            logger.error("Time coordinate not found in the dataset.")
        else:
            logger.info(f"Temporal Consistency: {temporal_consistency}")

def main():
    # Parse the command-line arguments
    args = parse_arguments()
    
    # Process a single file if --file is provided
    if args.file:
        logger.info(f"Processing file: {args.file}")
        process_file(args.file)
    
    # Process all supported files in a directory if --dir is provided
    if args.dir:
        logger.info(f"Processing directory: {args.dir}")
        for root, _, files in os.walk(args.dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.splitext(file)[1] in SUPPORTED_FORMATS:
                    logger.info(f"Processing file: {file_path}")
                    process_file(file_path)
                else:
                    logger.warning(f"Skipping unsupported file: {file_path}")

if __name__ == "__main__":
    main()

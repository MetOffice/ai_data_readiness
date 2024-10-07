import os
import logging
from tkinter import Tk, filedialog
import xarray as xr
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeatherClimateData:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.dataset = None

    def select_file(self):
        """Open a file dialog to select a file."""
        root = Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename(title="Select a weather and climate data file")
        logging.info(f"Selected file: {self.file_path}")
        return self.file_path

    def detect_gridded_format_and_open(self):
        """Detect the file format and open the dataset."""
        if not self.file_path:
            logging.error("No file path provided.")
            return None

        _, file_extension = os.path.splitext(self.file_path)
        format_engine_map = {
            '.nc': 'netcdf4',
            '.grib': 'cfgrib',
            '.h5': 'h5netcdf',
            '.hdf5': 'h5netcdf',
            '.tif': 'rasterio',
            '.tiff': 'rasterio',
            '.zarr': 'zarr',
        }

        if file_extension in format_engine_map:
            engine = format_engine_map[file_extension]
            try:
                self.dataset = xr.open_dataset(self.file_path, engine=engine)
                logging.info(f"Successfully opened {self.file_path} with engine {engine}")
                return self.dataset
            except Exception as e:
                logging.error(f"Failed to open {self.file_path} with engine {engine}: {e}")
                return None
        else:
            logging.error(f"Unsupported file format: {file_extension}")
            return None

    def get_spatial_resolution_and_coverage(self):
        """Get spatial resolution and coverage of the dataset."""
        if not self.dataset:
            logging.error("Dataset not loaded.")
            return None, None

        lat, lon = self._get_lat_lon_coords()
        if lat is None or lon is None:
            return None, None

        lat_res = np.abs(lat[1] - lat[0]).values if lat.size > 1 else None
        lon_res = np.abs(lon[1] - lon[0]).values if lon.size > 1 else None

        lat_min, lat_max = lat.min().values, lat.max().values
        lon_min, lon_max = lon.min().values, lon.max().values

        resolution = (lat_res, lon_res)
        coverage = {'latitude': (lat_min, lat_max), 'longitude': (lon_min, lon_max)}

        return resolution, coverage

    def get_temporal_resolution_and_coverage(self):
        """Get temporal resolution and coverage of the dataset."""
        if not self.dataset:
            logging.error("Dataset not loaded.")
            return None, None

        if 'time' not in self.dataset.coords:
            logging.error("Time coordinate not found in the dataset.")
            return None, None

        time = self.dataset['time']
        time_res = np.diff(time.values).astype('timedelta64[h]').astype(int)[0] if time.size > 1 else None
        time_min, time_max = time.min().values, time.max().values

        resolution = time_res
        # coverage = {'time': (time_min, time_max)}

        return resolution, coverage

    def check_spatial_consistency(self):
        """Check spatial consistency of the dataset."""
        if not self.dataset:
            logging.error("Dataset not loaded.")
            return None

        lat, lon = self._get_lat_lon_coords()
        if lat is None or lon is None:
            return None

        lat_diff = np.diff(lat.values)
        lon_diff = np.diff(lon.values)

        if not np.allclose(lat_diff, lat_diff[0]) or not np.allclose(lon_diff, lon_diff[0]):
            return False

        return True

    def check_temporal_consistency(self):
        """Check temporal consistency of the dataset."""
        if not self.dataset:
            logging.error("Dataset not loaded.")
            return None

        if 'time' not in self.dataset.coords:
            logging.error("Time coordinate not found in the dataset.")
            return None

        time = self.dataset['time']
        time_diff = np.diff(time.values).astype('timedelta64[h]').astype(int)

        if not np.allclose(time_diff, time_diff[0]):
            return False

        return True

    def _get_lat_lon_coords(self):
        """Helper function to get latitude and longitude coordinates."""
        if 'latitude' in self.dataset.coords and 'longitude' in self.dataset.coords:
            return self.dataset['latitude'], self.dataset['longitude']
        elif 'lat' in self.dataset.coords and 'lon' in self.dataset.coords:
            return self.dataset['lat'], self.dataset['lon']
        else:
            logging.error("Latitude and Longitude coordinates not found in the dataset.")
            return None, None

# Example usage
if __name__ == "__main__":
    wc_data = WeatherClimateData()
    wc_data.select_file()
    wc_data.detect_gridded_format_and_open()
    spatial_res, spatial_cov = wc_data.get_spatial_resolution_and_coverage()
    temporal_res, temporal_cov = wc_data.get_temporal_resolution_and_coverage()
    spatial_consistency = wc_data.check_spatial_consistency()
    temporal_consistency = wc_data.check_temporal_consistency()

    logging.info(f"Spatial Resolution: {spatial_res}")
    logging.info(f"Spatial Coverage: {spatial_cov}")
    logging.info(f"Temporal Resolution: {temporal_res}")
    logging.info(f"Temporal Coverage: {temporal_cov}")
    logging.info(f"Spatial Consistency: {spatial_consistency}")
    logging.info(f"Temporal Consistency: {temporal_consistency}")
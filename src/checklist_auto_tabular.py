import os
import logging
import argparse
import pandas as pd
import numpy as np
import json
from tqdm import tqdm

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = ['.csv', '.xlsx', '.xls', '.tsv']

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process and analyze tabular data.")
    
    parser.add_argument('--files', nargs='*', help="List of paths to tabular data files (CSV, Excel, TSV)")
    parser.add_argument('--dirs', nargs='*', help="List of directories containing tabular data files")
    parser.add_argument('--output', type=str, help="Path to save the analysis results in CSV or JSON format")
    
    parser.add_argument('--custom-nan', nargs='*', default=None, 
                        help="Custom NaN values to be treated as missing (e.g. -999 -9999)")
    parser.add_argument('--outlier-threshold', type=float, default=3.0, 
                        help="Z-score threshold for detecting outliers (default: 3.0)")

    args = parser.parse_args()
    
    if not args.files and not args.dirs:
        parser.error("Either --files or --dirs must be specified.")
    
    return args

def detect_tabular_format_and_open(file_path, custom_nan=None):
    """Detect the file format based on the file extension and open it with pandas."""
    _, file_extension = os.path.splitext(file_path)
    
    format_engine_map = {
        '.csv': pd.read_csv,
        '.xlsx': pd.read_excel,
        '.xls': pd.read_excel,
        '.tsv': lambda file: pd.read_csv(file, sep='\t'),
    }
    
    if file_extension not in format_engine_map:
        logger.error(f"Unsupported file format: {file_extension} for {file_path}")
        return None
    
    try:
        # Handle custom NaN values
        df = format_engine_map[file_extension](file_path, na_values=custom_nan)
        logger.info(f"Successfully opened {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error when opening {file_path}: {e}")
    
    return None

def check_missing_values(df):
    """Check for missing values in the dataset."""
    missing_values = df.isnull().sum().sum()
    
    if missing_values > 0:
        logger.warning(f"Missing values detected: {missing_values}")
        return missing_values
    
    logger.info("No missing values detected.")
    return 0

def check_column_consistency(df):
    """Check if data types in each column are consistent (e.g., no mixed data types)."""
    mixed_columns = {}
    
    for col in df.columns:
        if df[col].apply(lambda x: type(x)).nunique() > 1:
            mixed_columns[col] = df[col].apply(lambda x: type(x)).unique()
    
    if mixed_columns:
        logger.warning(f"Inconsistent data types found in columns: {mixed_columns}")
        return mixed_columns
    
    logger.info("No inconsistent data types found.")
    return None

def check_temporal_consistency(df, time_col='time'):
    """Check if temporal data is consistent (if applicable)."""
    if time_col in df.columns:
        try:
            df[time_col] = pd.to_datetime(df[time_col])
            time_diffs = df[time_col].diff().dropna()
            if not np.allclose(time_diffs.dt.total_seconds(), time_diffs.dt.total_seconds().mean()):
                logger.warning("Temporal resolution is not consistent.")
                return False
            
            logger.info("Temporal resolution is consistent.")
            return True
        except Exception as e:
            logger.error(f"Error checking temporal consistency: {e}")
            return None
    else:
        logger.info(f"Time column '{time_col}' not found.")
        return None

def check_outliers(df, threshold=3.0, numerical_cols=None):
    """Detect outliers in the dataset (using a Z-score method)."""
    if numerical_cols is None:
        numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    outliers = {}
    
    for col in numerical_cols:
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        outlier_count = (z_scores > threshold).sum()
        if outlier_count > 0:
            outliers[col] = outlier_count
    
    if outliers:
        logger.warning(f"Outliers detected in columns: {outliers}")
        return outliers
    
    logger.info("No outliers detected.")
    return None

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

def process_file(file_path, output_path=None, custom_nan=None, outlier_threshold=3.0):
    """Process a single tabular file."""
    df = detect_tabular_format_and_open(file_path, custom_nan=custom_nan)

    if df is not None:
        missing_values = check_missing_values(df)
        column_consistency = check_column_consistency(df)
        temporal_consistency = check_temporal_consistency(df)
        outliers = check_outliers(df, threshold=outlier_threshold)
        
        result = {
            'file': file_path,
            'missing_values': missing_values,
            'column_consistency': column_consistency,
            'temporal_consistency': temporal_consistency,
            'outliers': outliers
        }
        
        if output_path:
            save_results(result, output_path)
        
        return result

def process_directory(directory, output_path=None, custom_nan=None, outlier_threshold=3.0):
    """Process all supported files in a directory sequentially."""
    all_files = []
    for root, _, files in os.walk(directory):
        all_files.extend([os.path.join(root, f) for f in files if os.path.splitext(f)[1] in SUPPORTED_FORMATS])
    
    results = []
    with tqdm(total=len(all_files), desc="Processing files") as pbar:
        for file_path in all_files:
            result = process_file(file_path, output_path, custom_nan=custom_nan, outlier_threshold=outlier_threshold)
            if result:
                results.append(result)
            pbar.update(1)

    return results

def main():
    # Parse the command-line arguments
    args = parse_arguments()

    # Process files
    results = []
    if args.files:
        for file_path in args.files:
            logger.info(f"Processing file: {file_path}")
            result = process_file(file_path, args.output, custom_nan=args.custom_nan, outlier_threshold=args.outlier_threshold)
            if result:
                results.append(result)
    
    # Process directories
    if args.dirs:
        for directory in args.dirs:
            logger.info(f"Processing directory: {directory}")
            dir_results = process_directory(directory, args.output, custom_nan=args.custom_nan, outlier_threshold=args.outlier_threshold)
            results.extend(dir_results)

    if args.output:
        save_results(results, args.output)
    else:
        logger.info(f"Processing completed. Results: {results}")

if __name__ == "__main__":
    main()


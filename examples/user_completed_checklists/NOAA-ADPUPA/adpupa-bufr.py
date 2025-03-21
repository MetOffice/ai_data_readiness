# Python
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import netCDF4 as nc
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Set input data file name(s)
fname = "../../data/data_2021080100/gdas.t00z.adpupa.tm00_nc002001.nc"
print("Praveen checking fname = ", fname)

# Read input data file
ncd = nc.Dataset(fname, 'r')

# NetCDF global attributes
nc_attrs = ncd.ncattrs()
print('NetCDF Global Attributes: ')
print('nc_attrs = ', nc_attrs)
for nc_attr in nc_attrs:
    print('nc_attr:', ncd.getncattr(nc_attr))

# Dimension information
nc_dims = [dim for dim in ncd.dimensions]  # list of nc dimensions
print('nc_dims = ', nc_dims)
for dim in nc_dims:
    print(f'nc_dims {dim} length = {len(ncd.dimensions[dim])}')

# Variable information
lat = ncd.groups['MetaData'].variables['latitude'][:].ravel()
lon = ncd.groups['MetaData'].variables['longitude'][:].ravel()
dateTime = ncd.groups['MetaData'].variables['dateTime'][:].ravel()
stationElevation = ncd.groups['MetaData'].variables['stationElevation'][:].ravel()
stationIdentification = ncd.groups['MetaData'].variables['stationIdentification'][:].ravel()
pressure = ncd.groups['MetaData'].variables['pressure'][:].ravel()
airTemperature = ncd.groups['ObsValue'].variables['airTemperature'][:].ravel()
dewpointTemperature = ncd.groups['ObsValue'].variables['dewpointTemperature'][:].ravel()
windSpeed = ncd.groups['ObsValue'].variables['windSpeed'][:].ravel()
windDirection = ncd.groups['ObsValue'].variables['windDirection'][:].ravel()

# Create DataFrame
data = pd.DataFrame({
    'latitude': lat,
    'longitude': lon,
    'dateTime': dateTime,
    'stationElevation': stationElevation,
    'stationIdentification': stationIdentification,
    'pressure': pressure,
    'airTemperature': airTemperature,
    'dewpointTemperature': dewpointTemperature,
    'windSpeed': windSpeed,
    'windDirection': windDirection
})

# Statistical Analysis
# Descriptive statistics
print("\nDescriptive Statistics:\n", data.describe())

# Count missing values
missing_values_count = data.isnull().sum()
print("\nMissing Values Count:\n", missing_values_count)

# Replace Missing Values by Mean
# If pressure has missing values, fill them with the mean of the column
data['pressure'].fillna(data['pressure'].mean(), inplace=True)

# Recheck if there are still any missing values
missing_values_count_after_imputation = data.isnull().sum()
print("\nMissing Values Count After Imputation:\n", missing_values_count_after_imputation)

# Random Forest for Pressure Prediction
# Features and target
X = data[['latitude', 'longitude']]  # Features (lat, lon)
y = data['pressure']  # Target (pressure)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize RandomForestRegressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf.fit(X_train, y_train)

# Make predictions
y_pred = rf.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nMean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Plotting the Results
# Plot 1: Pressure vs Latitude and Longitude (scatter plot)
plt.figure(figsize=(10, 6))
scatter = plt.scatter(lon, lat, c=pressure, cmap='viridis', marker='o', s=10)
plt.colorbar(scatter, label='Pressure')
plt.title('Pressure Distribution Across Latitude and Longitude')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.savefig('pressure_distribution.png')
plt.show()

# Plot 2: Actual vs Predicted Pressure (Scatter plot)
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.title('Actual vs Predicted Pressure')
plt.xlabel('Actual Pressure')
plt.ylabel('Predicted Pressure')
plt.grid(True)
plt.savefig('actual_vs_predicted_pressure.png')
plt.show()

# Exit after completing all tasks
exit()


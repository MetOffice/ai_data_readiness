#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Set default path for DATA_READINESS_PATH if not set
if [ -z "$DATA_READINESS_PATH" ]; then
  echo "DATA_READINESS_PATH is not set. Setting it to the default path: $PWD"
  export DATA_READINESS_PATH="$PWD"
else
  echo "DATA_READINESS_PATH is set to: $DATA_READINESS_PATH"
fi

  # Ensure conda is initialized
if [ -z "$(which conda)" ]; then
  echo "Conda is not found. Please ensure conda is installed and added to your PATH."
  exit 1
fi

# Initialize conda for bash
eval "$(conda shell.bash hook)"

# Create the conda environment from the YML file
echo "Creating conda environment 'data_readiness'..."
conda env create --file envs/requirements.yml

# # Activate the conda environment
# source activate data_readiness || conda activate data_readiness

# Activate the conda environment
conda activate data_readiness

# Set up the IPython kernel
echo "Setting up IPython kernel for Jupyter Lab..."
python -m ipykernel install --user --name=data_readiness

echo "Setup complete. The 'data_readiness' environment is ready to use."

# Deactivate the conda environment
conda deactivate

# Log Anomaly Analysis

## Overview

This project aims to detect anomalies in system logs using machine learning techniques. It is designed to process raw log data (specifically HDFS logs), extract meaningful features, and train models to identify abnormal patterns that may indicate system failures or security threats.

## Project Structure

The project is organized as follows:

- **`data/`**: Storage for raw and processed data.
  - `raw/`: Contains original log files (e.g., `HDFS_2k.log`) and labels (`anomaly_label.csv`).
  - `processed/`: Stores parsed logs and feature matrices.
- **`notebooks/`**: Jupyter notebooks for interactive analysis and experimentation.
  - `01_data_exploration.ipynb`: Initial analysis of raw log data.
  - `02_feature_engineering.ipynb`: Prototyping feature extraction methods.
  - `03_model_training.ipynb`: Experimenting with different models.
- **`src/`**: Source code for the production pipeline.
  - `preprocess.py`: Scripts to parse and clean raw logs.
  - `feature_engineering.py`: Logic to convert logs into numerical features.
  - `train_model.py`: Script to train and save the anomaly detection model.
  - `detect_anomaly.py`: Inference script to detect anomalies in new data.
- **`models/`**: Directory to save trained model artifacts (e.g., serialized pickle files).
- **`results/`**: Output directory for analysis results, plots, and performance metrics.

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd Log_Anomaly_Analysis
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Data Processing
Run the preprocessing script to clean and parse the raw logs provided in `data/raw/`:
```bash
python src/preprocess.py
```

### 2. Feature Engineering
Transform the parsed logs into feature vectors suitable for machine learning:
```bash
python src/feature_engineering.py
```

### 3. Model Training
Train the anomaly detection model. This script will save the trained model to the `models/` directory:
```bash
python src/train_model.py
```

### 4. Anomaly Detection
Run the detection script on new log data or the test set:
```bash
python src/detect_anomaly.py
```

## Dataset

The project currently uses the HDFS log dataset sample (`HDFS_2k.log`) for development and testing. The ground truth labels for anomalies are available in `anomaly_label.csv`.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes.
4. Push to the branch and create a Pull Request.

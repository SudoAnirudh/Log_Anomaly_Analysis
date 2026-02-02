# Log Anomaly Analysis

## Overview

This project aims to detect anomalies in system logs using machine learning techniques. It processes raw HDFS logs, extracts features, and trains an Isolation Forest model to identify abnormal patterns.

## Project Structure

- **`data/`**: Storage for raw and processed data.
- **`notebooks/`**: Experimental Jupyter notebooks.
- **`src/`**: Production source code.
  - `preprocess.py`: Cleans and labels logs.
  - `feature_engineering.py`: Vectorizes logs.
  - `train_model.py`: Trains the model.
  - `detect_anomaly.py`: Runs inference.
- **`models/`**: Saved model artifacts.
- **`results/`**: Output predictions.
- **`main.py`**: CLI entry point for the pipeline.

## Getting Started

### Prerequisites

- Python 3.8+
- `pip`

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd Log_Anomaly_Analysis
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run Full Pipeline
To preprocess data, engineer features, and train the model in one go:
```bash
python main.py pipeline
```

### Run Individual Steps
```bash
python main.py preprocess
python main.py feature_engineering
python main.py train
```

### Anomaly Detection
To detect anomalies in a log file:
```bash
python main.py detect data/raw/HDFS_2k.log
```
Results will be saved to `results/anomaly_predictions.csv`.

## Dataset
The project includes a sample HDFS log dataset (`data/raw/HDFS_2k.log`) and labels (`data/raw/anomaly_label.csv`).

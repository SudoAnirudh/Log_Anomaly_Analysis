import pandas as pd
import re
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_LOG_PATH = os.path.join(BASE_DIR, "data", "raw", "HDFS_2k.log")
LABEL_PATH = os.path.join(BASE_DIR, "data", "raw", "anomaly_label.csv")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_labeled_logs.csv")

def extract_block_id(line):
    match = re.search(r'(blk_-?\d+)', line)
    return match.group(1) if match else None

def clean_log(line):
    # Remove numbers but keep block IDs intact for now (handled by specific replacement)
    # The notebook regex was:
    # line = re.sub(r'\d+', '', line)
    # line = re.sub(r'blk_-?\d+', 'BLK', line)
    
    # Let's follow the notebook exactly but be careful about order
    line = re.sub(r'\d+', '', line)
    line = re.sub(r'blk_-?\d+', 'BLK', line)
    return line.lower()

def preprocess():
    print("Loading raw logs...")
    if not os.path.exists(RAW_LOG_PATH):
        raise FileNotFoundError(f"Raw log file not found at {RAW_LOG_PATH}")
    
    logs = pd.read_csv(RAW_LOG_PATH, header=None)
    logs.columns = ["log"]
    
    print(f"Loaded {len(logs)} log lines.")

    # Extract Block ID
    print("Extracting Block IDs...")
    logs["block_id"] = logs["log"].apply(extract_block_id)
    logs = logs.dropna(subset=["block_id"])
    
    # Clean logs
    print("Cleaning logs...")
    logs["clean_log"] = logs["log"].apply(clean_log)
    
    # Group by Block ID
    print("Grouping logs by Block ID...")
    grouped_logs = logs.groupby("block_id")["clean_log"] \
                       .apply(lambda x: " ".join(x)) \
                       .reset_index()
    
    print(f"Total blocks found: {len(grouped_logs)}")
    
    # Load Labels
    print("Loading labels...")
    if not os.path.exists(LABEL_PATH):
        raise FileNotFoundError(f"Label file not found at {LABEL_PATH}")
        
    labels = pd.read_csv(LABEL_PATH)
    labels.columns = ["block_id", "label"]
    
    # Merge
    print("Merging logs and labels...")
    data = pd.merge(grouped_logs, labels, on="block_id", how="inner")
    
    print(f"Final dataset shape: {data.shape}")
    print("Sample data:")
    print(data.head())
    
    # Save
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    data.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Saved processed data to {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    preprocess()

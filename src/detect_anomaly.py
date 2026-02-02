import joblib
import re
import pandas as pd
import os
import argparse

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

def load_artifacts():
    try:
        model = joblib.load(os.path.join(MODELS_DIR, "isolation_forest_model.pkl"))
        vectorizer = joblib.load(os.path.join(MODELS_DIR, "vectorizer.pkl"))
        return model, vectorizer
    except FileNotFoundError as e:
        print(f"Error loading artifacts: {e}")
        print("Please ensure you have trained the model and saved the vectorizer.")
        return None, None

def clean_log(line):
    line = re.sub(r'\d+', '', line)
    line = re.sub(r'blk_-?\d+', 'BLK', line)
    return line.lower()

def detect_from_dataframe(logs_df):
    """
    Detect anomalies from a pandas DataFrame containing a 'log' column.
    Returns a DataFrame with columns: ['block_id', 'anomaly', 'log', 'clean_log']
    """
    model, vectorizer = load_artifacts()
    if not model or not vectorizer:
        return None

    # Preprocess
    def extract_block_id(line):
        match = re.search(r'(blk_-?\d+)', line)
        return match.group(1) if match else None

    # Working on a copy to avoid SettingWithCopy warnings if slice passed
    logs = logs_df.copy()
    
    if "block_id" not in logs.columns:
        logs["block_id"] = logs["log"].apply(extract_block_id)

    logs = logs.dropna(subset=["block_id"])
    if logs.empty:
         print("No valid blocks found.")
         return pd.DataFrame()

    logs["clean_log"] = logs["log"].apply(clean_log)
    
    grouped_logs = logs.groupby("block_id")["clean_log"] \
                       .apply(lambda x: " ".join(x)) \
                       .reset_index()
    
    if grouped_logs.empty:
        print("No blocks found.")
        return pd.DataFrame()

    # Vectorize
    try:
        X = vectorizer.transform(grouped_logs["clean_log"])
    except Exception as e:
        print(f"Vectorization failed: {e}")
        return pd.DataFrame()
    
    # Predict
    preds = model.predict(X)
    # -1 is anomaly, 1 is normal
    
    results = pd.DataFrame({
        "block_id": grouped_logs["block_id"],
        "anomaly": preds
    })
    
    return results

def detect(log_file):
    if not os.path.exists(log_file):
        print(f"File not found: {log_file}")
        return

    print(f"Processing {log_file}...")
    try:
        # Read logs (assuming single column file or raw logs)
        logs = pd.read_csv(log_file, header=None)
        logs.columns = ["log"]
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    results = detect_from_dataframe(logs)
    
    if results is None or results.empty:
        print("No results returned.")
        return

    anomalies = results[results["anomaly"] == -1]
    
    print(f"Total Blocks: {len(results)}")
    print(f"Anomalies Found: {len(anomalies)}")
    
    if not anomalies.empty:
        print("\nPredicted Anomalies:")
        print(anomalies)
        
        # Save results
        out_path = os.path.join(BASE_DIR, "results", "anomaly_predictions.csv")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        anomalies.to_csv(out_path, index=False)
        print(f"\nSaved anomalies to {out_path}")
    else:
        print("No anomalies detected.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect anomalies in log file")
    parser.add_argument("logfile", help="Path to raw log file")
    args = parser.parse_args()
    
    detect(args.logfile)

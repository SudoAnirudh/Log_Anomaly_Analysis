import argparse
import sys
import os

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.preprocess import preprocess
from src.feature_engineering import feature_engineering
from src.train_model import train_model
from src.detect_anomaly import detect

def run_pipeline():
    print("========================================")
    print("Starting Post-Processing Pipeline")
    print("========================================")
    
    print("\n[Step 1/3] Preprocessing...")
    preprocess()
    
    print("\n[Step 2/3] Feature Engineering...")
    feature_engineering()
    
    print("\n[Step 3/3] Model Training...")
    train_model()
    
    print("\n========================================")
    print("Pipeline Completed Successfully!")
    print("========================================")

def main():
    parser = argparse.ArgumentParser(description="Log Anomaly Analysis CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Pipeline command
    subparsers.add_parser("pipeline", help="Run the full training pipeline (preprocess -> feature_eng -> train)")
    
    # Individual step commands
    subparsers.add_parser("preprocess", help="Run data preprocessing only")
    subparsers.add_parser("feature_engineering", help="Run feature engineering only")
    subparsers.add_parser("train", help="Run model training only")
    
    # Detect command
    detect_parser = subparsers.add_parser("detect", help="Detect anomalies in a log file")
    detect_parser.add_argument("logfile", help="Path to log file for detection")
    
    args = parser.parse_args()
    
    if args.command == "pipeline":
        run_pipeline()
    elif args.command == "preprocess":
        preprocess()
    elif args.command == "feature_engineering":
        feature_engineering()
    elif args.command == "train":
        train_model()
    elif args.command == "detect":
        detect(args.logfile)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

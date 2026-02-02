import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_OUT_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

def train_model():
    print("Loading feature matrices...")
    try:
        X_train = joblib.load(os.path.join(PROCESSED_OUT_DIR, "X_train.pkl"))
        print(f"Loaded X_train: {X_train.shape}")
    except FileNotFoundError:
        print("Feature matrices not found. Run feature_engineering.py first.")
        return

    print("Training Isolation Forest...")
    # Parameters from notebook: n_estimators=150, contamination=0.05, random_state=42
    model = IsolationForest(
        n_estimators=150,
        contamination=0.05,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train)
    print("Model trained.")

    print("Saving model...")
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODELS_DIR, "isolation_forest_model.pkl"))
    print(f"Model saved to {os.path.join(MODELS_DIR, 'isolation_forest_model.pkl')}")

if __name__ == "__main__":
    train_model()

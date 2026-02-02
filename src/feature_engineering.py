import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import joblib
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_labeled_logs.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
PROCESSED_OUT_DIR = os.path.join(BASE_DIR, "data", "processed")

def feature_engineering():
    print("Loading processed data...")
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Processed data not found at {PROCESSED_DATA_PATH}. Run preprocess.py first.")
        
    data = pd.read_csv(PROCESSED_DATA_PATH)
    
    # Handle NaN values in clean_log if any (though preprocess should have handled it)
    if data["clean_log"].isnull().any():
        print("Warning: Found NaN values in clean_log. Filling with empty string.")
        data["clean_log"] = data["clean_log"].fillna("")

    print(f"Dataset shape: {data.shape}")
    print(data["label"].value_counts())

    print("Vectorizing logs...")
    vectorizer = CountVectorizer(
        max_features=500,
        stop_words='english'
    )
    
    X = vectorizer.fit_transform(data["clean_log"])
    y = data["label"]
    
    print(f"Feature matrix shape: {X.shape}")

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Saving artifacts...")
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(PROCESSED_OUT_DIR, exist_ok=True)

    joblib.dump(X_train, os.path.join(PROCESSED_OUT_DIR, "X_train.pkl"))
    joblib.dump(X_test, os.path.join(PROCESSED_OUT_DIR, "X_test.pkl"))
    joblib.dump(y_train, os.path.join(PROCESSED_OUT_DIR, "y_train.pkl"))
    joblib.dump(y_test, os.path.join(PROCESSED_OUT_DIR, "y_test.pkl"))
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, "vectorizer.pkl"))
    
    print("✅ Feature engineering completed and saved.")

if __name__ == "__main__":
    feature_engineering()

# 🛡️ Log Anomaly Detection System

![Banner](docs/images/banner.png)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 📖 Overview

**Log Anomaly Detection** is an AI-powered system designed to identify abnormal patterns in system logs (specifically HDFS logs). By leveraging **Machine Learning (Isolation Forest)**, it automatically detects potential failures or security threats that traditional rule-based systems might miss.

This project offers both a **Command Line Interface (CLI)** for automated pipelines and a **Streamlit Web GUI** for interactive analysis.

---

## ✨ Features

- **🚀 Automated Pipeline**: seamless preprocessing, feature engineering, and model training.
- **🤖 AI-Powered Detection**: Uses unsupervised learning (Isolation Forest) to find unknown anomalies.
- **📊 Interactive Dashboard**: User-friendly GUI to paste logs or upload files for instant analysis.
- **📁 HDFS Log Support**: Specialized parsing for Hadoop Distributed File System logs.
- **📈 Detailed Reporting**: Exports anomaly reports to CSV.

---

## 📸 Demo

### Interactive GUI
*Paste logs directly or upload files to detect anomalies instantly.*

![GUI Demo](docs/images/demo.webp)

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/SudoAnirudh/Log_Anomaly_Analysis.git
    cd Log_Anomaly_Analysis
    ```

2.  **Set Up Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 Usage

### 🖥️ Streamlit GUI (Recommended)
Launch the interactive web application:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### ⌨️ Command Line Interface (CLI)

You can check all available commands using:
```bash
python main.py --help
```

#### 1. Run Full Training Pipeline
Preprocess data, extract features, and train the model in one step:
```bash
python main.py pipeline
```

#### 2. Detect Anomalies in a File
Run inference on a new log file:
```bash
python main.py detect data/raw/HDFS_2k.log
```
*Results will be saved to `results/anomaly_predictions.csv`.*

#### 3. Run Individual Steps
```bash
python main.py preprocess
python main.py feature_engineering
python main.py train
```

---

## 📂 Project Structure

| File/Directory | Description |
| :--- | :--- |
| `app.py` | Streamlit GUI application entry point. |
| `main.py` | CLI entry point for the pipeline. |
| `src/` | Source code for preprocessing, training, and detection. |
| `data/` | Directory for raw and processed datasets. |
| `models/` | Saved trained model artifacts (`.pkl`). |
| `results/` | Output directory for detection results. |
| `notebooks/` | Jupyter notebooks for experimentation. |

---

## 🔮 Future Improvements

- [ ] Support for real-time log streaming (Kafka/Fluentd).
- [ ] Deep Learning models (LSTM/Transformer) for sequence analysis.
- [ ] Docker containerization for easy deployment.

---

Made with ❤️ by Anirudh

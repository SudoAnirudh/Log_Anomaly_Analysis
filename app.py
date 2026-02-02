import streamlit as st
import pandas as pd
import io
import sys
import os

# Add src to python path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from detect_anomaly import detect_from_dataframe

st.set_page_config(
    page_title="Log Anomaly Detection",
    page_icon="🔍",
    layout="wide"
)

def run_detection(df):
    with st.spinner("Analyzing logs..."):
        results = detect_from_dataframe(df)
        
    if results is None:
        st.error("Failed to load model artifacts. Ensure models/ directory exists.")
        return

    if results.empty:
        st.warning("No valid blocks found in the logs.")
        return

    anomalies = results[results["anomaly"] == -1]
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Blocks", len(results))
    col2.metric("Anomalies Found", len(anomalies))
    col3.metric("Anomaly Rate", f"{(len(anomalies)/len(results))*100:.2f}%")
    
    # Results
    if not anomalies.empty:
        st.error(f"⚠️ {len(anomalies)} anomalies detected!")
        with st.expander("View Anomalies", expanded=True):
            st.dataframe(anomalies, use_container_width=True)
            
            # Download
            csv = anomalies.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Anomalies CSV",
                csv,
                "anomalies.csv",
                "text/csv",
                key='download-csv'
            )
    else:
        st.success("✅ No anomalies detected.")

def main():
    st.title("🔍 Log Anomaly Detection System")
    st.markdown("Upload a log file or paste log entries to detect anomalies using Isolation Forest.")

    # Sidebar
    st.sidebar.header("Options")
    input_method = st.sidebar.radio("Input Method", ["Paste Logs", "Upload File"])

    # Main Area
    if input_method == "Paste Logs":
        log_text = st.text_area("Paste Log Data Here:", height=300, placeholder="081109 203615 148 INFO dfs.DataNode$PacketResponder: PacketResponder 1 for block blk_38865049064139660 terminating")
        if st.button("Analyze Logs"):
            if log_text.strip():
                # Convert text to dataframe
                data = io.StringIO(log_text)
                try:
                    df = pd.read_csv(data, header=None, sep="\\n") # Read as single column
                    df.columns = ["log"]
                    run_detection(df)
                except Exception as e:
                    st.error(f"Error processing input: {e}")
            else:
                st.warning("Please paste some logs first.")

    elif input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload Log File", type=["log", "txt", "csv"])
        if uploaded_file is not None:
            if st.button("Analyze File"):
                try:
                    # Depending on file type, might need different reads
                    # Assuming raw log file without header
                    df = pd.read_csv(uploaded_file, header=None)
                    # If multiple columns, try to assume the whole line is the log or take the last column?
                    # For HDFS, it's unstructured text usually, so read_csv might split by commas if any.
                    # Better to read as lines.
                    
                    # Reset stream and read lines
                    uploaded_file.seek(0)
                    lines = uploaded_file.read().decode("utf-8").splitlines()
                    df = pd.DataFrame(lines, columns=["log"])
                    
                    run_detection(df)
                except Exception as e:
                    st.error(f"Error reading file: {e}")

if __name__ == "__main__":
    main()

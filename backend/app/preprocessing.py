import pandas as pd
import os

LOG_FILE = "logs/raw_traffic_log.csv"
OUTPUT_FILE = "logs/preprocessed_data.csv"

# Ensure the backend directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

async def preprocess_data():
    try:
        if not os.path.exists(LOG_FILE):
            return {"error": "Raw traffic log file not found. Please start packet capture first."}

        df = pd.read_csv(LOG_FILE)

        # Ensure timestamp is in datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('timestamp', inplace=True)

        # Aggregate data into 5-second intervals
        df_aggregated = df.resample('5s').agg({
            'data_length': 'sum',
            'src_ip': 'count',
        }).rename(columns={'src_ip': 'packet_count', 'data_length': 'total_data_transferred'})

        df_aggregated.to_csv(OUTPUT_FILE)
        return {"message": f"Data preprocessing complete. Saved to {OUTPUT_FILE}."}
    except Exception as e:
        return {"error": str(e)}

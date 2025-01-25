import pandas as pd

LOG_FILE = "backend/raw_traffic_log.csv"
OUTPUT_FILE = "backend/preprocessed_data.csv"

async def preprocess_data():
    # Read raw traffic data
    try:
        df = pd.read_csv(LOG_FILE)
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('datetime', inplace=True)

        # Aggregate data into 5-second intervals
        df_aggregated = df.resample('5S').agg({
            'data_length': 'sum',
            'src_ip': 'count',
        }).rename(columns={'src_ip': 'packet_count', 'data_length': 'total_data_transferred'})

        # Save aggregated data
        df_aggregated.to_csv(OUTPUT_FILE)
        return {"message": f"Data preprocessing complete. Saved to {OUTPUT_FILE}."}
    except Exception as e:
        return {"error": str(e)}

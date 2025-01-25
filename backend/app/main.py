import os
import csv
from fastapi import FastAPI, BackgroundTasks
from app.data_collection import create_log_file, start_packet_capture, pause_capture, resume_capture, stop_capture
from app.preprocessing import preprocess_data

app = FastAPI()

# Ensure the log file exists on startup
create_log_file()

# Helper function to check if there is any data in the log file
def check_csv_data(file_path):
    if not os.path.exists(file_path):
        return False  # File does not exist

    try:
        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file)
            headers = next(reader, None)  # Skip headers
            for row in reader:
                if all(field.strip() for field in row):  # Check if all columns have data
                    return True
        return False  # No data or rows with missing fields
    except Exception as e:
        return False  # Error while reading the file

# POST endpoint to start packet capture
@app.post("/start-capture/")
async def start_capture(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_packet_capture, "Wi-Fi")  # Replace 'Wi-Fi' with your actual network interface
    return {"message": "Packet capture started in the background."}

# POST endpoint to start data preprocessing
@app.post("/preprocess-data/")
async def preprocess(background_tasks: BackgroundTasks):
    background_tasks.add_task(preprocess_data)
    return {"message": "Data preprocessing started in the background."}

# GET endpoint to check if the raw traffic log file exists and contains data
@app.get("/check-log/")
async def check_log_file():
    log_file = "logs/raw_traffic_log.csv"
    
    if os.path.exists(log_file):
        has_data = check_csv_data(log_file)
        if has_data:
            return {"message": "Log file exists and contains data."}
        else:
            return {"message": "Log file exists, but it is empty or has missing data."}
    else:
        return {"message": "Log file does not exist."}

# GET endpoint to check if the preprocessed data file exists and contains data
@app.get("/check-preprocessed/")
async def check_preprocessed():
    preprocessed_file = "logs/preprocessed_data.csv"
    
    if os.path.exists(preprocessed_file):
        has_data = check_csv_data(preprocessed_file)
        if has_data:
            return {"message": "Preprocessed data file exists and contains data."}
        else:
            return {"message": "Preprocessed data file exists, but it is empty or has missing data."}
    else:
        return {"message": "Preprocessed data file does not exist."}
    
# POST endpoint to pause packet capture
@app.post("/pause-capture/")
async def pause_capture_endpoint():
    pause_capture()
    return {"message": "Packet capture paused."}

# POST endpoint to resume packet capture
@app.post("/resume-capture/")
async def resume_capture_endpoint():
    resume_capture()
    return {"message": "Packet capture resumed."}

# POST endpoint to stop packet capture
@app.post("/stop-capture/")
async def stop_capture_endpoint():
    stop_capture()
    return {"message": "Packet capture stopped."}

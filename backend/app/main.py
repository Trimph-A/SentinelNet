from fastapi import FastAPI, BackgroundTasks
from app.data_collection import create_log_file, start_packet_capture_async
from app.preprocessing import preprocess_data
import os

app = FastAPI()

# Ensure the log file exists on startup
create_log_file()

@app.post("/start-capture/")
async def start_capture(background_tasks: BackgroundTasks):
    # Use the function from data_collection to start packet capture in the background
    background_tasks.add_task(start_packet_capture_async, "Wi-Fi")
    return {"message": "Packet capture started in the background."}

@app.post("/preprocess-data/")
async def preprocess(background_tasks: BackgroundTasks):
    # Start the preprocessing task in the background (adjust to your preprocessing logic)
    background_tasks.add_task(preprocess_data)
    return {"message": "Data preprocessing started in the background."}

@app.get("/check-log/") 
async def check_log_file():
    if os.path.exists("logs/raw_traffic_log.csv"):
        return {"message": "Log file exists."}
    return {"message": "Log file does not exist."}

@app.get("/check-preprocessed/")
async def check_preprocessed():
    if os.path.exists("logs/preprocessed_data.csv"):
        return {"message": "Preprocessed data file exists."}
    return {"message": "Preprocessed data file does not exist."}

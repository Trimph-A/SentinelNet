from fastapi import FastAPI, BackgroundTasks
from app.data_collection import start_capture
from app.preprocessing import preprocess_data

app = FastAPI()

# Define the root path
@app.get("/")
async def root():
    return {"message": "Welcome to the SentinelNet API"}

# FastAPI route to start packet capture in the background
@app.post("/start-capture/")
async def start_packet_capture(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_capture)
    return {"message": "Packet capture started in the background."}

@app.post("/preprocess-data/")
async def process_data():
    return await preprocess_data()

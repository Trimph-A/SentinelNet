from fastapi import FastAPI, BackgroundTasks
from scapy.all import sniff, IP, TCP, UDP, ICMP
import os
import time
import uuid
import logging

app = FastAPI()

# Define the log file for captured traffic
LOG_FILE = "backend/raw_traffic_log.csv"

# Create a logger for more detailed logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to start capturing packets with more detailed information
def start_packet_capture():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("timestamp,unique_id,src_ip,dst_ip,protocol,src_port,dst_port,data_length,flags,packet_size\n")
    
    def packet_callback(packet):
        try:
            # Add unique ID to each packet for easy traceability
            unique_id = str(uuid.uuid4())

            # Get packet details
            timestamp = packet.time
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto
            src_port = packet[IP].sport if TCP in packet or UDP in packet else None
            dst_port = packet[IP].dport if TCP in packet or UDP in packet else None
            flags = packet.sprintf("%IP.flags%")
            data_length = len(packet)
            packet_size = len(packet)

            # Write packet details to the log file
            with open(LOG_FILE, "a") as f:
                f.write(f"{timestamp},{unique_id},{src_ip},{dst_ip},{protocol},{src_port},{dst_port},{data_length},{flags},{packet_size}\n")
            
            # Log the captured packet (optional for debugging)
            logger.info(f"Captured packet: {src_ip} -> {dst_ip} | Protocol: {protocol} | Size: {packet_size} bytes")
        
        except Exception as e:
            logger.error(f"Error processing packet: {str(e)}")
    
    # Start sniffing the network for packets
    sniff(prn=packet_callback, store=0, filter="ip", timeout=60)  # Sniffing for 60 seconds as an example

# FastAPI route to start packet capture in the background
@app.post("/start-capture/")
async def start_capture(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_packet_capture)
    return {"message": "Packet capture started in the background."}


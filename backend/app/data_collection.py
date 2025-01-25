import asyncio
import os
import csv
import uuid
import logging
from scapy.all import sniff
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOG_FILE = "logs/raw_traffic_log.csv"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Flags and Events for control
capture_paused = False
capture_running = False
capture_event = threading.Event()  # Event to manage pause/resume
capture_event.set()  # Initially set to allow capture to run

# Function to create and write headers to the CSV file if it doesn't exist
def create_log_file():
    try:
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "timestamp", "unique_id", "src_ip", "dst_ip", "protocol",
                    "src_port", "dst_port", "packet_size", "info", "flags", "packet_type"
                ])
            logger.info(f"Log file {LOG_FILE} created with headers.")
        else:
            logger.info(f"Log file {LOG_FILE} already exists.")
    except Exception as e:
        logger.error(f"Error creating log file: {str(e)}")

# Function to process and log packets captured by scapy
def packet_callback(packet):
    global capture_running
    try:
        # Wait for resume signal if capture is paused
        capture_event.wait()

        if not capture_running:
            logger.info("Capture stopped.")
            return False  # Stop sniffing

        # Extract packet details
        unique_id = str(uuid.uuid4())
        timestamp = packet.time
        src_ip = packet[1].src if packet.haslayer('IP') else None
        dst_ip = packet[1].dst if packet.haslayer('IP') else None
        protocol = packet.proto if packet.haslayer('IP') else None
        src_port = packet.sport if packet.haslayer('TCP') or packet.haslayer('UDP') else None
        dst_port = packet.dport if packet.haslayer('TCP') or packet.haslayer('UDP') else None
        packet_size = len(packet)
        info = packet.summary() if hasattr(packet, "summary") else "N/A"

        # Additional info for detecting issues
        flags = packet.flags if hasattr(packet, "flags") else "N/A"
        packet_type = packet.name if hasattr(packet, "name") else "N/A"
        
        # Log packet data to the CSV file
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, unique_id, src_ip, dst_ip, protocol,
                             src_port, dst_port, packet_size, info, flags, packet_type])
        logger.info(f"Captured packet: {src_ip} -> {dst_ip} | Protocol: {protocol} | Size: {packet_size} bytes | Flags: {flags} | Type: {packet_type}")
    except Exception as e:
        logger.error(f"Error processing packet: {str(e)}")

# Blocking function to start capturing packets using scapy
def start_packet_capture(interface="any"):
    global capture_running
    capture_running = True
    logger.info("Starting packet capture...")
    try:
        sniff(iface=interface, prn=packet_callback, store=0, stop_filter=lambda x: not capture_running)  # Pass stop_filter to sniff
    except Exception as e:
        logger.error(f"Error during packet capture: {str(e)}")
        capture_running = False

# Function to pause the capture
def pause_capture():
    global capture_paused
    capture_paused = True
    capture_event.clear()  # This will pause the capture (clear event)
    logger.info("Capture paused.")

# Function to resume the capture
def resume_capture():
    global capture_paused
    capture_paused = False
    capture_event.set()  # This will resume the capture (set event)
    logger.info("Capture resumed.")

# Function to stop the capture
def stop_capture():
    global capture_running
    capture_running = False  # This will stop the sniffing loop
    logger.info("Capture stopped.")

# This is a helper function to run the packet capture in an async event loop
async def start_packet_capture_async(interface="any"):
    try:
        logger.info(f"Starting packet capture on interface: {interface}")
        loop = asyncio.get_event_loop()
        if loop.is_running():
            logger.info("Event loop is already running.")
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Run the blocking capture in a background thread using asyncio.to_thread
        await asyncio.to_thread(start_packet_capture, interface)
    except Exception as e:
        logger.error(f"Error starting packet capture asynchronously: {str(e)}")

# Start the asyncio event loop and call the capture function
def run_async_capture(interface="any"):
    asyncio.run(start_packet_capture_async(interface))

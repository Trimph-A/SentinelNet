import pyshark
import os
import csv
import uuid
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the log file and ensure the directory exists
LOG_FILE = "logs/raw_traffic_log.csv"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

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

# Function to process and log packets captured by pyshark
def packet_callback(packet):
    try:
        # Extract basic information from the packet
        unique_id = str(uuid.uuid4())
        timestamp = packet.sniff_time
        src_ip = packet.ip.src if hasattr(packet, "ip") else None
        dst_ip = packet.ip.dst if hasattr(packet, "ip") else None
        protocol = packet.transport_layer if hasattr(packet, "transport_layer") else None
        src_port = packet[packet.transport_layer].srcport if protocol in ("TCP", "UDP") else None
        dst_port = packet[packet.transport_layer].dstport if protocol in ("TCP", "UDP") else None
        packet_size = packet.length
        info = packet.info if hasattr(packet, "info") else "N/A"

        # Additional data for monitoring (for detecting hacks/malfunctions)
        flags = packet.tcp.flags if hasattr(packet, "tcp") else "N/A"
        packet_type = packet.highest_layer if hasattr(packet, "highest_layer") else "N/A"

        # Log captured packet data
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, unique_id, src_ip, dst_ip, protocol, 
                src_port, dst_port, packet_size, info, flags, packet_type
            ])

        logger.info(f"Captured packet: {src_ip} -> {dst_ip} | Protocol: {protocol} | Size: {packet_size} bytes | Flags: {flags} | Type: {packet_type}")
    except Exception as e:
        logger.error(f"Error processing packet: {str(e)}")

# Blocking function to start capturing packets using pyshark
def start_packet_capture(interface="any"):
    logger.info("Starting packet capture...")
    try:
        capture = pyshark.LiveCapture(interface=interface)
        capture.apply_on_packets(packet_callback)
    except Exception as e:
        logger.error(f"Error during packet capture: {str(e)}")

# Create a new asyncio event loop for packet capture and run it in a separate thread
async def start_packet_capture_async(interface="any"):
    try:
        logger.info(f"Starting packet capture on interface: {interface}")
        # Create an event loop specifically for the packet capture task
        loop = asyncio.new_event_loop()  # Create a new event loop
        asyncio.set_event_loop(loop)  # Set it as the current event loop

        # Run the blocking function in a separate thread using asyncio.to_thread
        await asyncio.to_thread(start_packet_capture, interface)
    except Exception as e:
        logger.error(f"Error starting packet capture asynchronously: {str(e)}")

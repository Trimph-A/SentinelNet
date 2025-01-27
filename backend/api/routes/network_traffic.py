from fastapi import APIRouter, HTTPException
from api.models.traffic import TrafficData
from api.models.notifications import AnomalyNotification
from api.services.llama_model import llama_model
from api.services.blockchain_notifier import blockchain_notifier
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/v1")

# Helper function for preprocessing network traffic data
def preprocess_traffic_data(traffic_data: List[TrafficData]):
    # Preprocess the raw traffic data into a format compatible with the LLaMA model
    return [data.dict() for data in traffic_data]

# Main endpoint for network traffic processing
@router.post("/network_traffic")
def process_network_traffic(traffic_data: List[TrafficData]):
    """Endpoint for receiving network traffic data."""
    try:
        # Step 1: Preprocess the data
        preprocessed_data = preprocess_traffic_data(traffic_data)

        # Step 2: Analyze the data using the LLaMA model
        anomalies = llama_model.analyze(preprocessed_data)

        # Step 3: For each anomaly, enhance analysis using RAG
        notifications = []
        for anomaly in anomalies:
            # Enhance the anomaly information using RAG
            enhanced_info = retrieve_and_generate(anomaly['evidence'])

            # Create a notification object
            notification = AnomalyNotification(
                event_type=anomaly['event_type'],
                description=f"{anomaly['description']} - Additional Context: {enhanced_info}",
                timestamp=datetime.utcnow(),
                evidence=anomaly['evidence'],
                security=anomaly['security']
            )

            # Send the notification to the blockchain testnet
            blockchain_notifier.send_notification(notification.dict())
            notifications.append(notification)

        return {
            "status": "success",
            "anomalies_detected": len(notifications),
            "details": notifications
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the app
app.include_router(router)

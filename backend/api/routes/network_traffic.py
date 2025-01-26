from fastapi import APIRouter, HTTPException
from api.models.traffic import TrafficData
from api.models.notifications import AnomalyNotification
from api.services.llama_model import llama_model
from api.services.blockchain_notifier import blockchain_notifier
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/v1")

@router.post("/network_traffic")
def process_network_traffic(traffic_data: List[TrafficData]):
    """Endpoint for receiving network traffic data."""
    try:
        # Step 1: Preprocess the data
        preprocessed_data = preprocess_traffic_data(traffic_data)

        # Step 2: Analyze the data using LLaMA model
        anomalies = llama_model.analyze(preprocessed_data)

        # Step 3: Generate and send blockchain notifications for detected anomalies
        notifications = []
        for anomaly in anomalies:
            notification = AnomalyNotification(
                event_type=anomaly['event_type'],
                description=anomaly['description'],
                timestamp=datetime.utcnow(),
                evidence=anomaly['evidence'],
                security=anomaly['security']
            )
            
            # Send notification to blockchain testnet
            blockchain_notifier.send_notification(notification.dict())
            notifications.append(notification)

        return {"status": "success", "anomalies_detected": len(notifications), "details": notifications}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

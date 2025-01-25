from pydantic import BaseModel
from datetime import datetime

class AnomalyNotification(BaseModel):
    event_type: str
    description: str
    timestamp: datetime
    evidence: str
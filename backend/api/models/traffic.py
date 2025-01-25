from pydantic import BaseModel
from datetime import datetime

class TrafficData(BaseModel):
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    data_transferred: int
    timestamp: datetime


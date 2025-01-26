from pydantic import BaseModel

class TrafficData(BaseModel):
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    data_transferred: int
    timestamp: str

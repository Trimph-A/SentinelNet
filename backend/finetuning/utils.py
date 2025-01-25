def preprocess_traffic_data(traffic_data: List[TrafficData]):
    """Aggregate and preprocess traffic data for model analysis."""
    aggregated_data = [
        {
            "source_ip": data.source_ip,
            "destination_ip": data.destination_ip,
            "total_data": data.data_transferred,
            "protocol": data.protocol,
        }
        for data in traffic_data
    ]
    return aggregated_data
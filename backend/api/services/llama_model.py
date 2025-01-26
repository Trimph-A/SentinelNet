from typing import List
from api.models.traffic import TrafficData
from api.models.notifications import AnomalyNotification
from rag.rag_integration import RAGHandler


class LlamaModel:
    def __init__(self, rag_handler: RAGHandler):
        self.rag_handler = rag_handler

    def analyze(self, traffic_logs: List[TrafficData]):
        try:
            # Prepare the input prompt for the Llama model
            prompt = self._generate_prompt(traffic_logs)

            # Use RAG to analyze the logs
            response = self.rag_handler.analyze_logs(prompt)

            # Process the response to detect anomalies
            anomalies = self._parse_response(response)

            return anomalies
        except Exception as e:
            raise RuntimeError(f"Error during Llama model analysis: {str(e)}")

    def _generate_prompt(self, traffic_logs: List[TrafficData]) -> str:
        """Generate a structured prompt for the Llama model."""
        prompt = "Analyze the following network traffic logs and identify vulnerabilities or anomalies. Respond with a structured JSON format.\nLogs:\n"
        for log in traffic_logs:
            prompt += f"- Source IP: {log.src_ip}, Destination IP: {log.dst_ip}, " \
                      f"Source Port: {log.src_port}, Destination Port: {log.dst_port}, Protocol: {log.protocol}, " \
                      f"Data Transferred: {log.data_length}, Timestamp: {log.time_diff}, Label: {log.label}\n"
        return prompt

    def _parse_response(self, response: dict) -> List[AnomalyNotification]:
        """Parse the Llama model response and create anomaly notifications."""
        anomalies = []
        for item in response.get("anomalies", []):
            anomaly = AnomalyNotification(
                event_type=item["event_type"],
                severity=item["severity"],
                details=item["details"],
                timestamp=item["timestamp"],
            )
            anomalies.append(anomaly)
        return anomalies

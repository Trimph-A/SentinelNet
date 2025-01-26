from typing import List
from datetime import datetime
from api.models.traffic import TrafficData
from api.models.notifications import AnomalyNotification
from RAG.rag_integration import RAGHandler

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
        prompt = "Analyze the following network traffic logs and identify vulnerabilities or anomalies. Respond with a structured JSON format."\
                 " Logs: \n"
        for log in traffic_logs:
            prompt += f"- Source IP: {log.source_ip}, Destination IP: {log.destination_ip}, " \
                     f"Source Port: {log.source_port}, Destination Port: {log.destination_port}, Protocol: {log.protocol}, " \
                     f"Data Transferred: {log.data_transferred}, Timestamp: {log.timestamp}\n"
        return prompt

    def _parse_response(self, response: dict) -> List[AnomalyNotification]:
        """Parse the Llama model response and create anomaly notifications."""
        anomalies = []
        for item in response.get("anomalies", []):
            anomaly = AnomalyNotification(
                event_type=item["event_type"],
                description=item["description"],
                timestamp=datetime.utcnow(),
                evidence=item["evidence"]
            )
            anomalies.append(anomaly)
        return anomalies

# Initialize the RAG handler
rag_handler = RAGHandler()

# Instantiate the Llama model
llama_model = LlamaModel(rag_handler)
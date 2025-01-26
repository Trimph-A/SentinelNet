import json
from openai.embeddings_utils import get_embedding
import faiss
from config import load_config


class RAGHandler:
    def __init__(self, dataset_path="dataset.json"):
        """Initializes the RAGHandler with FAISS index and OpenAI client configuration."""
        config = load_config("config/config.yaml")
        self.index = faiss.IndexFlatL2(768)  # Dimensionality of the embeddings
        self.embeddings = []
        self.metadata = []
        self.client = OpenAI(
            api_key=config["api"]["aimlapi_key"],
            base_url=config["api"]["aimlapi_base_url"],
        )
        self.load_dataset(dataset_path)

    def load_dataset(self, dataset_path: str):
        """Loads dataset from a JSON file and indexes it."""
        try:
            with open(dataset_path, "r") as file:
                logs = json.load(file)
                if not isinstance(logs, list):
                    raise ValueError("Dataset must be a list of log entries.")
                self.add_to_index(logs)
                print(f"Loaded and indexed {len(logs)} logs from {dataset_path}.")
        except Exception as e:
            raise RuntimeError(f"Error loading dataset: {str(e)}")

    def add_to_index(self, logs: list):
        """Generates embeddings and adds logs to the FAISS index."""
        for log in logs:
            embedding = get_embedding(json.dumps(log))
            self.index.add([embedding])
            self.embeddings.append(embedding)
            self.metadata.append(log)

    def query_index(self, query: str, k: int = 5) -> list:
        """Retrieves the top-k closest logs to the query."""
        query_embedding = get_embedding(query)
        distances, indices = self.index.search([query_embedding], k)
        return [self.metadata[i] for i in indices[0]]

    def analyze_logs(self, prompt: str) -> dict:
        """Uses the Llama model via RAG to analyze network traffic logs."""
        try:
            response = self.client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant specialized in analyzing network traffic logs "
                            "to identify vulnerabilities and anomalies. Respond with structured JSON output."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                max_tokens=3000,
                temperature=0.7,
            )
            raw_content = response["choices"][0]["message"]["content"]
            return json.loads(raw_content)
        except Exception as e:
            raise RuntimeError(f"Error during RAG log analysis: {str(e)}")

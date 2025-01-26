import json
from openai import OpenAI
from config import load_config


class RAGHandler:
    def __init__(self):
        """Initializes the RAGHandler with OpenAI client configuration."""
        config = load_config("config/config.yaml")
        self.client = OpenAI(
            api_key=config["api"]["aimlapi_key"],
            base_url=config["api"]["aimlapi_base_url"],
        )

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

            # Extract and parse JSON content from the response
            raw_content = response["choices"][0]["message"]["content"]
            return json.loads(raw_content)

        except Exception as e:
            raise RuntimeError(f"Error during RAG log analysis: {str(e)}") from e

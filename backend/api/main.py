from fastapi import FastAPI
from .routes.network_traffic import router

app = FastAPI(
    title="Router Traffic Analysis API",
    description=(
        "An API designed to monitor and analyze network traffic from routers using a pretrained "
        "LLaMA 3.2:1B model. The system automatically detects and processes patterns, generating "
        "insights that are sent as notifications to a blockchain for secure and transparent tracking."
    ),
    version="1.0.0",
)

app.include_router(router)

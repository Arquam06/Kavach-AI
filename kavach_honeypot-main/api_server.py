from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from agent.controller import run_agent

# App initialization

app = FastAPI(title="KAVACH Honeypot API")
@app.get("/")
def home():
    return {
        "message": "KAVACH Honeypot API is running",
        "docs": "/docs",
        "honeypot_endpoint": "/honeypot"
    }


# Simple API Key (for tester)

VALID_API_KEY = "test-kavach-key"

# Request schema

class HoneypotRequest(BaseModel):
    message: str

# Honeypot Endpoint

@app.post("/honeypot")
def honeypot_endpoint(
    request: HoneypotRequest,
    x_api_key: str = Header(None)
):
    #Authentication check
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    #Run your existing agent
    result = run_agent(request.message)

    result["extracted_intelligence"] = {
        k: list(v) for k, v in result["extracted_intelligence"].items()
    }

    return result
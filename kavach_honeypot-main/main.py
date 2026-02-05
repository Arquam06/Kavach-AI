from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from agent.controller import run_agent

app = FastAPI(title="KAVACH Honeypot API")

VALID_API_KEY = "test-kavach-key"

class HoneypotRequest(BaseModel):
    message: str = "No message provided"


@app.get("/")
def home():
    return RedirectResponse(url="/docs")


@app.post("/honeypot")
def honeypot_endpoint(
    payload: HoneypotRequest = None,
    x_api_key: str = Header(...)
):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    if payload is None:
        payload = HoneypotRequest()

    result = run_agent(payload.message)

    result["extracted_intelligence"] = {
        k: list(v) for k, v in result["extracted_intelligence"].items()
    }

    return result

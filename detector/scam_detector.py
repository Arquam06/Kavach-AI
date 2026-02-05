from config import (
    URGENCY_KEYWORDS,
    FINANCIAL_KEYWORDS,
    THREAT_KEYWORDS
)

def detect_scam(message: str) -> dict:
    message = message.lower()
    score = 0.0

    if any(word in message for word in URGENCY_KEYWORDS):
        score += 0.3

    if any(word in message for word in FINANCIAL_KEYWORDS):
        score += 0.4

    if any(word in message for word in THREAT_KEYWORDS):
        score += 0.2

    if "http" in message or "www" in message:
        score += 0.3

    score = min(score, 1.0)

    return {
        "is_scam": score >= 0.6,
        "confidence": round(score, 2)
    }
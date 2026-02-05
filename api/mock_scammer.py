def send_to_scammer(agent_message: str) -> str:
    msg = agent_message.lower()

    if "upi" in msg:
        return "Send payment to securepay@upi immediately"

    if "link" in msg or "verify" in msg:
        return "Verify here http://secure-bank-verification.com"

    return "Your account is blocked, act fast!"
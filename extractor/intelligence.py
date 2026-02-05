import regex as re

UPI_REGEX = r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}"
BANK_REGEX = r"\b\d{10,16}\b"
URL_REGEX = r"https?://[^\s]+"

def extract_intelligence(message: str, data: dict) -> dict:
    upis = re.findall(UPI_REGEX, message)
    banks = re.findall(BANK_REGEX, message)
    urls = re.findall(URL_REGEX, message)

    data["upi_ids"].update(upis)
    data["bank_accounts"].update(banks)
    data["phishing_links"].update(urls)

    return data
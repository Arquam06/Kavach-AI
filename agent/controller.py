import random
from detector.scam_detector import detect_scam
from agent.persona import PERSONA_PROFILES
from agent.responder import generate_reply_llm
from extractor.intelligence import extract_intelligence
from api.mock_scammer import send_to_scammer
from config import MAX_CONVERSATION_TURNS, PERSONAS


def is_repeated_reply(conversation_log, new_reply, threshold=2):
    replies = [
        turn["scammer"]
        for turn in conversation_log
        if "scammer" in turn
    ]
    return replies.count(new_reply) >= threshold


def run_agent(initial_message: str) -> dict:
    detection = detect_scam(initial_message)

    result = {
        "is_scam": detection["is_scam"],
        "confidence": detection["confidence"],
        "persona": None,
        "extracted_intelligence": {
            "upi_ids": set(),
            "bank_accounts": set(),
            "phishing_links": set()
        },
        "conversation_log": []
    }

    if not detection["is_scam"]:
        return result

    persona_name = random.choice(PERSONAS)
    persona = PERSONA_PROFILES[persona_name]
    result["persona"] = persona_name

    result["conversation_log"].append({"scammer": initial_message})
    last_message = initial_message

    for _ in range(MAX_CONVERSATION_TURNS):

        agent_reply = generate_reply_llm(
            persona_name,
            persona,
            result["conversation_log"],
            last_message
        )
        result["conversation_log"].append({"agent": agent_reply})

        scammer_reply = send_to_scammer(agent_reply)
        result["conversation_log"].append({"scammer": scammer_reply})

        result["extracted_intelligence"] = extract_intelligence(
            scammer_reply,
            result["extracted_intelligence"]
        )

        if any(result["extracted_intelligence"].values()):
            break

      
        if is_repeated_reply(result["conversation_log"], scammer_reply):
            result["conversation_log"].append({
                "agent": "I will verify this with my bank and get back later."
            })
            break

        last_message = scammer_reply

    if not any(result["extracted_intelligence"].values()):
        result["conversation_log"].append({
            "agent": "I need to check this from my side first."
        })

    return result

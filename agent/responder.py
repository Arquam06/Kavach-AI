import random

def generate_reply_llm(persona_name, persona, conversation_log, last_message):
    """
    MOCK AGENTIC AI
    - No API
    - No repetition
    - Persona + intent driven
    - Honeypot safe
    """

    last_message = last_message.lower()

    used_agent_messages = {
        turn["agent"] for turn in conversation_log if "agent" in turn
    }

    # High-value extraction pushes (non-repeating)
    high_value_prompts = [
        ("upi", "Please confirm the exact UPI ID, I don’t want to make a mistake."),
        ("http", "Before clicking, can you confirm this is the official website?"),
        ("www", "Before clicking, can you confirm this is the official website?"),
        ("account", "Which bank is this from? I need to check my records."),
        ("bank", "Which bank is this from? I need to check my records."),
        ("blocked", "What caused this issue suddenly? I was using it earlier today."),
        ("suspended", "What caused this issue suddenly? I was using it earlier today."),
        ("pay", "Is there any reference number or confirmation I should note?"),
        ("transfer", "Is there any reference number or confirmation I should note?")
    ]

    for keyword, reply in high_value_prompts:
        if keyword in last_message and reply not in used_agent_messages:
            return reply

    # Persona-driven strategy
    strategy = persona.get("strategy", [])

    persona_questions = {
        "ask for clarification": [
            "Can you explain this a bit more clearly?",
            "I’m not fully understanding what went wrong."
        ],
        "seek reassurance": [
            "Will this be resolved once I complete the steps?",
            "Is my money safe right now?"
        ],
        "request verification details": [
            "Can you send me the official details?",
            "Is there a message or reference ID for this?"
        ],
        "ask impact-related questions": [
            "Will my transactions stop because of this?",
            "Is this affecting all payments or only incoming ones?"
        ],
        "request official payment details": [
            "Please share the payment or verification details.",
            "Where exactly should I complete this process?"
        ],
        "push for quick resolution": [
            "What is the fastest way to resolve this?",
            "I need this fixed urgently for my work."
        ],
        "ask if message is genuine": [
            "Is this really from the bank?",
            "How do I know this is official?"
        ],
        "request step-by-step help": [
            "Can you guide me step by step?",
            "What should I do first?"
        ]
    }

    possible_replies = []
    for step in strategy:
        possible_replies.extend(persona_questions.get(step, []))

    possible_replies = [
        r for r in possible_replies if r not in used_agent_messages
    ]

    if possible_replies:
        return random.choice(possible_replies)

    # Graceful disengagement fallback
    fallback_responses = [
        "I need some time to verify this from my side.",
        "Let me confirm this with my bank before proceeding.",
        "I’ll get back once I verify the details.",
        "This is confusing, I need to double-check first."
    ]

    return random.choice(fallback_responses)
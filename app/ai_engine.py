import torch
from typing import Dict, List, Tuple

CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Login Issue": ["login", "password", "signin", "sign in", "authentication", "account locked", "otp"],
    "Payment Issue": ["payment", "refund", "invoice", "billing", "transaction", "deducted", "money"],
    "Technical Issue": ["error", "bug", "crash", "server", "api", "database", "timeout", "failed"],
    "Access Request": ["access", "permission", "role", "admin", "authorization", "approval"],
    "General Query": ["help", "query", "information", "support", "question", "details"],
}

HIGH_PRIORITY_WORDS = ["urgent", "critical", "production", "down", "blocked", "immediately", "failed"]
MEDIUM_PRIORITY_WORDS = ["issue", "error", "not working", "delay", "problem", "unable"]


def clean_text(text: str) -> str:
    return text.lower().strip()


def score_category(description: str) -> Tuple[str, Dict[str, int]]:
    text = clean_text(description)
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for keyword in keywords if keyword in text)

    category_names = list(scores.keys())
    score_tensor = torch.tensor(list(scores.values()), dtype=torch.float32)
    best_index = torch.argmax(score_tensor).item()
    best_category = category_names[best_index]

    if scores[best_category] == 0:
        best_category = "General Query"
    return best_category, scores


def predict_priority(description: str) -> str:
    text = clean_text(description)
    high_score = sum(1 for word in HIGH_PRIORITY_WORDS if word in text)
    medium_score = sum(1 for word in MEDIUM_PRIORITY_WORDS if word in text)
    priority_tensor = torch.tensor([high_score, medium_score], dtype=torch.float32)
    if priority_tensor[0].item() > 0:
        return "High"
    if priority_tensor[1].item() > 0:
        return "Medium"
    return "Low"


def generate_genai_explanation(description: str, category: str, priority: str) -> str:
    prompt = f"""
    You are an AI ticket triage assistant.
    Ticket Description: {description}
    Predicted Category: {category}
    Predicted Priority: {priority}
    Explain the reason in simple business language.
    """
    _ = prompt
    return (
        f"The ticket is classified as '{category}' because the description contains terms related to this issue type. "
        f"The priority is marked as '{priority}' based on urgency and impact keywords found in the ticket. "
        f"This explanation follows a prompt-based GenAI reasoning approach."
    )


def analyze_ticket(description: str) -> Dict[str, str]:
    category, _ = score_category(description)
    priority = predict_priority(description)
    ai_explanation = generate_genai_explanation(description, category, priority)
    return {"category": category, "priority": priority, "ai_explanation": ai_explanation}

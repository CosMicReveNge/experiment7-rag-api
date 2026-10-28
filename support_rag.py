import os

# Store sample customer support information.
KNOWLEDGE_BASE = {
    "refund": "Customers can request a refund within 7 days of purchase.",
    "delivery": "Standard delivery usually takes 3 to 5 business days.",
    "payment": "Customers can pay using credit cards, debit cards, or UPI.",
    "support": "Customer support is available Monday to Friday, 9 AM to 6 PM."
}


def generate_answer(question):
    # Simulate a backend failure when testing error handling.
    if os.getenv("MOCK_BACKEND_FAIL", "false").lower() == "true":
        raise RuntimeError("Simulated backend failure")

    # Find information relevant to the customer's question.
    question = question.lower()
    for keyword, answer in KNOWLEDGE_BASE.items():
        if keyword in question:
            return answer

    # Avoid inventing information not found in the knowledge base.
    return "I do not have enough information to answer this question."

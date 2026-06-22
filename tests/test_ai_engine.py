from app.ai_engine import analyze_ticket


def test_login_high_priority_ticket():
    result = analyze_ticket("Production users are unable to login urgently")
    assert result["category"] == "Login Issue"
    assert result["priority"] == "High"


def test_payment_ticket():
    result = analyze_ticket("Payment deducted but invoice not generated")
    assert result["category"] == "Payment Issue"


def test_default_general_query():
    result = analyze_ticket("I need some details about my request")
    assert result["category"] == "General Query"

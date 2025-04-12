"""
Simple tests for risk scoring logic without database dependencies.
"""
import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.logic.risk_scoring import compute_risk_score

def test_high_risk_calculation():
    """Test high risk calculation."""
    # High risk scenario: high debt, negative profit, bad news
    score, level, explanations = compute_risk_score(
        user_id="test_user",
        company_name="High Risk Corp",
        debt_to_equity=3.0,
        net_profit=-5000,
        negative_news_score=0.9,
        late_payments_rate=0.2,
        sector="general"
    )
    
    # Assertions
    assert score > 0.6, "High risk scenario should have score > 0.6"
    assert level == "High Risk", "Expected 'High Risk' recommendation"
    assert len(explanations) >= 3, "Should have at least 3 risk factors"
    assert "High debt-to-equity ratio" in explanations
    assert "Negative profitability" in explanations
    assert "Significant negative news" in explanations

def test_low_risk_calculation():
    """Test low risk calculation."""
    # Low risk scenario: low debt, positive profit, no bad news
    score, level, explanations = compute_risk_score(
        user_id="test_user",
        company_name="Low Risk Corp",
        debt_to_equity=1.0,
        net_profit=5000,
        negative_news_score=0.1,
        late_payments_rate=0.05,
        sector="general"
    )
    
    # Assertions
    assert score < 0.4, "Low risk scenario should have score < 0.4"
    assert level == "Low Risk", "Expected 'Low Risk' recommendation"
    assert len(explanations) == 0, "Should have no risk factors" 
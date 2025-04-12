"""
Unit tests for risk scoring logic.
"""
import pytest
from app.logic.risk_scoring import compute_risk_score

def test_compute_risk_score_high_risk():
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
    assert "High late payments rate" in explanations

def test_compute_risk_score_low_risk():
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

def test_compute_risk_score_sector_specific():
    """Test sector-specific risk calculation."""
    # Test high-volatility sector
    score1, level1, explanations1 = compute_risk_score(
        user_id="test_user",
        company_name="Energy Corp",
        debt_to_equity=1.5,
        net_profit=1000,
        negative_news_score=0.3,
        sector="oil"
    )
    
    # Same parameters but different sector
    score2, level2, explanations2 = compute_risk_score(
        user_id="test_user",
        company_name="Tech Corp",
        debt_to_equity=1.5,
        net_profit=1000,
        negative_news_score=0.3,
        sector="technology"
    )
    
    # Assertions
    assert score1 > score2, "High-volatility sector should increase risk score"
    assert "High-volatility sector" in explanations1
    assert "High-volatility sector" not in explanations2

def test_compute_risk_score_score_capping():
    """Test that risk score is capped at 1.0."""
    # Extreme risk scenario with multiple severe factors
    score, level, explanations = compute_risk_score(
        user_id="test_user",
        company_name="Extreme Risk Corp",
        debt_to_equity=5.0,
        net_profit=-10000,
        negative_news_score=1.0,
        late_payments_rate=0.5,
        sector="oil",
        additional_factors={"countryRisk": 0.9}
    )
    
    # Assertions
    assert score <= 1.0, "Risk score should be capped at 1.0"
    assert level == "High Risk", "Expected 'High Risk' recommendation"
    assert len(explanations) >= 4, "Should have many risk factors"

def test_compute_risk_score_with_additional_factors():
    """Test risk calculation with additional factors."""
    # Additional factors included
    score, level, explanations = compute_risk_score(
        user_id="test_user",
        company_name="Additional Factors Corp",
        debt_to_equity=1.5,
        net_profit=2000,
        negative_news_score=0.3,
        additional_factors={"countryRisk": 0.8, "marketShare": 0.05}
    )
    
    # Currently additional factors don't affect the score in our implementation
    # but we test that they're properly handled
    assert isinstance(score, float), "Should return a valid float score"
    assert isinstance(level, str), "Should return a valid risk level string"
    assert isinstance(explanations, list), "Should return a list of explanations" 
"""
Risk calculation engine module.

This module provides the core algorithms for calculating business risk scores
based on financial metrics, operational performance, and external factors.
"""
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime
import logging
import math

logger = logging.getLogger(__name__)

# Weights for different risk factors
WEIGHTS = {
    "debt_to_equity": 0.30,
    "net_profit": 0.25,
    "negative_news": 0.20,
    "late_payments": 0.25
}

# Sector adjustment factors (multipliers)
SECTOR_ADJUSTMENTS = {
    "technology": 1.0,
    "healthcare": 0.9,
    "finance": 1.2,
    "retail": 1.1,
    "manufacturing": 1.05,
    "energy": 1.3,
    "oil": 1.3,
    "gas": 1.3,
    "real_estate": 1.15,
    "telecommunications": 0.95,
    "utilities": 0.85,
    "consumer_goods": 1.0,
    "general": 1.0  # Default
}

def compute_risk_score(
    user_id: str, 
    company_name: str,
    debt_to_equity: float,
    net_profit: float,
    negative_news_score: float,
    late_payments_rate: float = 0.0,
    sector: str = "general",
    additional_factors: Optional[Dict[str, Any]] = None
) -> Tuple[float, str, List[str]]:
    """
    Compute a risk score based on financial and other risk factors.
    
    Args:
        user_id: Unique identifier for the requesting user
        company_name: Name of the company being evaluated
        debt_to_equity: Debt to equity ratio
        net_profit: Net profit amount
        negative_news_score: Score representing negative news (0-1)
        late_payments_rate: Rate of late payments (0-1)
        sector: Business sector
        additional_factors: Any additional factors to consider
        
    Returns:
        Tuple containing:
        - risk_score (float): 0-100 score where higher means riskier
        - risk_level (str): "Low Risk", "Medium Risk", or "High Risk"
        - explanations (List[str]): List of factors contributing to the score
    """
    logger.info(f"Computing risk score for company: {company_name} (user: {user_id})")
    
    explanations = []
    
    # Calculate individual factor scores (0-1 scale)
    debt_factor = calculate_debt_to_equity_factor(debt_to_equity, explanations)
    profit_factor = calculate_net_profit_factor(net_profit, explanations)
    news_factor = calculate_negative_news_factor(negative_news_score, explanations)
    payments_factor = calculate_late_payments_factor(late_payments_rate, explanations)
    
    # Calculate weighted base score
    base_score = (
        WEIGHTS["debt_to_equity"] * debt_factor +
        WEIGHTS["net_profit"] * profit_factor +
        WEIGHTS["negative_news"] * news_factor +
        WEIGHTS["late_payments"] * payments_factor
    ) / sum(WEIGHTS.values())
    
    # Apply sector adjustment
    sector_key = sector.lower()
    sector_multiplier = SECTOR_ADJUSTMENTS.get(sector_key, SECTOR_ADJUSTMENTS["general"])
    
    if sector_multiplier > 1.0:
        explanations.append(f"{sector.capitalize()} sector has higher than average baseline risk")
    elif sector_multiplier < 1.0:
        explanations.append(f"{sector.capitalize()} sector has lower than average baseline risk")
    else:
        explanations.append(f"{sector.capitalize()} sector has moderate baseline risk")
    
    # Calculate final score (0-100 scale)
    final_score = base_score * sector_multiplier * 100
    
    # Cap the score at 100
    if final_score > 100:
        final_score = 100.0
        logger.debug("Score capped at 100.0")
    
    # Process additional factors if provided
    if additional_factors:
        for factor, value in additional_factors.items():
            logger.debug(f"Processing additional factor: {factor} = {value}")
            # Additional logic can be added here for custom factors
    
    # Determine risk level
    if final_score >= 71:
        risk_level = "High Risk"
    elif final_score >= 41:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"
    
    logger.info(f"Risk calculation completed for {company_name}. Score: {final_score:.1f}, Level: {risk_level}")
    
    return final_score, risk_level, explanations

def calculate_debt_to_equity_factor(debt_to_equity: float, explanations: List[str]) -> float:
    """
    Calculate risk factor for debt-to-equity ratio.
    
    Args:
        debt_to_equity: The debt-to-equity ratio
        explanations: List to append explanations to
        
    Returns:
        Risk factor value between 0-1
    """
    if debt_to_equity <= 1.0:
        explanations.append("Debt-to-equity ratio is within healthy range")
        return 0.2
    elif debt_to_equity <= 2.0:
        explanations.append("Debt-to-equity ratio indicates moderate financial leverage")
        return 0.5
    elif debt_to_equity <= 3.0:
        explanations.append("High debt-to-equity ratio increases financial risk")
        return 0.7
    else:
        explanations.append("Very high debt-to-equity ratio indicates significant financial leverage")
        return 1.0

def calculate_net_profit_factor(net_profit: float, explanations: List[str]) -> float:
    """
    Calculate risk factor for net profit.
    
    Args:
        net_profit: The net profit amount
        explanations: List to append explanations to
        
    Returns:
        Risk factor value between 0-1
    """
    if net_profit > 500000:
        explanations.append("Strong positive net profit indicates excellent financial health")
        return 0.1
    elif net_profit > 100000:
        explanations.append("Positive net profit indicates good financial health")
        return 0.3
    elif net_profit > 0:
        explanations.append("Modest positive net profit")
        return 0.5
    elif net_profit > -100000:
        explanations.append("Negative net profit shows concerning financial performance")
        return 0.7
    else:
        explanations.append("Significant losses indicate serious financial challenges")
        return 1.0

def calculate_negative_news_factor(negative_news_score: float, explanations: List[str]) -> float:
    """
    Calculate risk factor for negative news coverage.
    
    Args:
        negative_news_score: Score between 0-1 representing negative news coverage
        explanations: List to append explanations to
        
    Returns:
        Risk factor value between 0-1
    """
    if negative_news_score <= 0.2:
        explanations.append("Low negative news coverage")
        return 0.2
    elif negative_news_score <= 0.4:
        explanations.append("Moderate negative news coverage")
        return 0.5
    elif negative_news_score <= 0.6:
        explanations.append("Negative press coverage may impact business reputation")
        return 0.7
    else:
        explanations.append("High negative news coverage suggests significant reputational risk")
        return 1.0

def calculate_late_payments_factor(late_payments_rate: float, explanations: List[str]) -> float:
    """
    Calculate risk factor for late payments rate.
    
    Args:
        late_payments_rate: Rate between 0-1 representing late payments
        explanations: List to append explanations to
        
    Returns:
        Risk factor value between 0-1
    """
    if late_payments_rate <= 0.05:
        explanations.append("Low rate of late payments suggests good cash flow management")
        return 0.1
    elif late_payments_rate <= 0.1:
        explanations.append("Moderate rate of late payments")
        return 0.4
    elif late_payments_rate <= 0.2:
        explanations.append("Elevated late payments rate may indicate cash flow issues")
        return 0.7
    else:
        explanations.append("High rate of late payments suggests cash flow problems")
        return 1.0

def get_risk_recommendations(risk_level: str, score: float, sector: str) -> List[str]:
    """
    Generate recommendations based on risk level, score, and sector.
    
    Args:
        risk_level: The calculated risk level
        score: The calculated risk score
        sector: The business sector
        
    Returns:
        List of recommendations
    """
    recommendations = []
    
    if risk_level == "High Risk":
        recommendations.append("Conduct immediate comprehensive financial review")
        recommendations.append("Develop debt reduction strategy")
        recommendations.append("Implement stricter accounts receivable policies")
        
        if sector.lower() in ["retail", "manufacturing"]:
            recommendations.append("Review inventory management to improve cash flow")
        
        if score > 85:
            recommendations.append("Consider external financial expertise/restructuring")
    
    elif risk_level == "Medium Risk":
        recommendations.append("Quarterly financial health monitoring recommended")
        recommendations.append("Develop action plan for identified risk areas")
        
        if sector.lower() in ["technology", "finance"]:
            recommendations.append("Evaluate competitive positioning in volatile market")
    
    else:  # Low Risk
        recommendations.append("Maintain current financial practices")
        recommendations.append("Annual risk reassessment recommended")
    
    return recommendations 
"""
Risk scoring logic module.
"""
from typing import Dict, Any, Tuple, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def compute_risk_score(
    user_id: str, 
    company_name: str,
    debt_to_equity: float,
    net_profit: float,
    negative_news_score: float,
    late_payments_rate: float = 0.0,
    sector: str = "general",
    additional_factors: Dict[str, Any] = None
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
        - risk_score (float): 0-1 score where higher means riskier
        - risk_level (str): "Low Risk", "Medium Risk", or "High Risk"
        - explanations (List[str]): List of factors contributing to the score
    """
    logger.info(f"Computing risk score for company: {company_name} (user: {user_id})")
    
    score = 0.0
    explanations = []
    
    # Process debt to equity ratio
    if debt_to_equity > 2:
        score += 0.3
        explanations.append("High debt-to-equity ratio")
        logger.debug(f"Added 0.3 to risk score due to high debt-to-equity ratio: {debt_to_equity}")
    
    # Process net profit
    if net_profit < 0:
        score += 0.2
        explanations.append("Negative profitability")
        logger.debug(f"Added 0.2 to risk score due to negative profit: {net_profit}")
    
    # Process negative news
    if negative_news_score > 0.5:
        score += 0.2
        explanations.append("Significant negative news")
        logger.debug(f"Added 0.2 to risk score due to negative news: {negative_news_score}")
    
    # Process late payments
    if late_payments_rate > 0.1:
        score += 0.15
        explanations.append("High late payments rate")
        logger.debug(f"Added 0.15 to risk score due to late payments: {late_payments_rate}")
    
    # Process sector-specific risks
    if sector.lower() in ["oil", "gas", "energy"]:
        score += 0.1
        explanations.append("High-volatility sector")
        logger.debug(f"Added 0.1 to risk score due to high-volatility sector: {sector}")
    
    # Process additional factors
    if additional_factors:
        for factor, value in additional_factors.items():
            logger.debug(f"Processing additional factor: {factor} = {value}")
            # Additional logic can be added here
    
    # Cap the score at 1.0
    if score > 1:
        score = 1.0
        logger.debug("Score capped at 1.0")
    
    # Determine risk level
    if score >= 0.7:
        risk_level = "High Risk"
    elif score >= 0.4:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"
    
    logger.info(f"Risk calculation completed for {company_name}. Score: {score}, Level: {risk_level}")
    
    return score, risk_level, explanations 
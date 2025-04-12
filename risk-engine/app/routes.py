"""
API routes for the Risk Engine.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from .database import get_db, test_connection
from .models import RiskEvaluation
from .logic.risk_calculator import compute_risk_score, get_risk_recommendations
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Risk Engine"])

class RiskRequest(BaseModel):
    """Data model for risk scoring requests."""
    user_id: str
    companyName: str
    debtToEquity: float
    netProfit: float
    negativeNewsScore: float
    latePaymentsRate: float = 0.0
    sector: str = "general"
    additionalFactors: Dict[str, Any] = {}
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "companyName": "Acme Corp",
                "debtToEquity": 2.5,
                "netProfit": -1000,
                "negativeNewsScore": 0.8,
                "latePaymentsRate": 0.2,
                "sector": "technology",
                "additionalFactors": {
                    "yearsInBusiness": 3,
                    "countryRisk": 0.3
                }
            }
        }


class RiskResponse(BaseModel):
    """Data model for risk scoring responses."""
    score: float
    explanations: List[str]
    recommendation: str
    recommendations: List[str]
    evaluation_id: Optional[int] = None


@router.post("/evaluate", response_model=RiskResponse)
def evaluate_risk(req: RiskRequest, db: Session = Depends(get_db)):
    """
    Calculate a risk score based on the provided company data.
    
    Args:
        req: The request data containing company information
        db: Database session
        
    Returns:
        A risk assessment with score and contributing factors
    """
    logger.info(f"Risk evaluation requested for company: {req.companyName}")
    
    try:
        # Calculate the risk score using the enhanced risk calculator
        score, risk_level, explanations = compute_risk_score(
            user_id=req.user_id,
            company_name=req.companyName,
            debt_to_equity=req.debtToEquity,
            net_profit=req.netProfit,
            negative_news_score=req.negativeNewsScore,
            late_payments_rate=req.latePaymentsRate,
            sector=req.sector,
            additional_factors=req.additionalFactors
        )
        
        # Get specific recommendations based on the risk assessment
        recommendations = get_risk_recommendations(risk_level, score, req.sector)
        
        # Store the evaluation in the database
        try:
            db_evaluation = RiskEvaluation(
                user_id=req.user_id,  # Also store the user_id
                company_name=req.companyName,
                sector=req.sector,
                debt_to_equity=req.debtToEquity,
                net_profit=req.netProfit,
                negative_news_score=req.negativeNewsScore,
                late_payments_rate=req.latePaymentsRate,
                risk_score=score,
                recommendation=risk_level,
                explanations=explanations
            )
            db.add(db_evaluation)
            db.commit()
            db.refresh(db_evaluation)
            evaluation_id = db_evaluation.id
            logger.info(f"Stored evaluation with ID {evaluation_id}")
        except Exception as e:
            logger.error(f"Error storing evaluation: {e}")
            db.rollback()
            evaluation_id = None
        
        return {
            "score": score,
            "explanations": explanations,
            "recommendation": risk_level,
            "recommendations": recommendations,
            "evaluation_id": evaluation_id
        }
    
    except Exception as e:
        logger.error(f"Error calculating risk score: {e}")
        raise HTTPException(status_code=500, detail=f"Error calculating risk score: {str(e)}")


@router.get("/evaluations/{evaluation_id}")
def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific risk evaluation by ID"""
    evaluation = db.query(RiskEvaluation).filter(RiskEvaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    # Generate recommendations for historical evaluation
    recommendations = get_risk_recommendations(
        evaluation.recommendation, 
        evaluation.risk_score, 
        evaluation.sector
    )
    
    # Convert to dict to add recommendations
    result = evaluation.__dict__.copy()
    if "_sa_instance_state" in result:
        del result["_sa_instance_state"]
    
    result["recommendations"] = recommendations
    
    return result


@router.get("/evaluations/company/{company_name}")
def get_company_evaluations(company_name: str, db: Session = Depends(get_db)):
    """Retrieve all risk evaluations for a specific company"""
    evaluations = db.query(RiskEvaluation).filter(
        RiskEvaluation.company_name == company_name
    ).all()
    
    return evaluations


@router.get("/health")
def health_check():
    """Health check endpoint with database connection test"""
    db_status = "connected" if test_connection() else "disconnected"
    logger.info(f"Health check called. Database status: {db_status}")
    
    return {
        "status": "healthy",
        "database": db_status
    } 
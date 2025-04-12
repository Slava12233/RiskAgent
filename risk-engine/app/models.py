"""
Database models for the Risk Engine.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
import json
from .database import Base, DATABASE_URL

# Use different column type for explanations based on database type
# SQLite doesn't support JSON type, so we use Text and handle serialization
is_sqlite = DATABASE_URL.startswith('sqlite')

class RiskEvaluation(Base):
    """
    Model for storing risk evaluation results.
    """
    __tablename__ = "risk_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # User who requested the evaluation
    company_name = Column(String, index=True)
    sector = Column(String, index=True)
    debt_to_equity = Column(Float)
    net_profit = Column(Float)
    negative_news_score = Column(Float)
    late_payments_rate = Column(Float)
    risk_score = Column(Float)
    recommendation = Column(String)
    
    # Use Text for SQLite, handle JSON serialization/deserialization in properties
    explanations_json = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    @property
    def explanations(self):
        """Deserialize JSON data from Text field."""
        if self.explanations_json:
            return json.loads(self.explanations_json)
        return []
    
    @explanations.setter
    def explanations(self, value):
        """Serialize list to JSON string."""
        self.explanations_json = json.dumps(value)
    
    def __repr__(self):
        return f"<RiskEvaluation(id={self.id}, user={self.user_id}, company={self.company_name}, score={self.risk_score})>" 
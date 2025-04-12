# Risk Engine Documentation

## Overview

Risk Engine is a specialized API service designed to evaluate business risks based on financial and operational metrics. The system computes risk scores and provides detailed recommendations to help businesses understand their risk exposure and make informed decisions.

## System Architecture

### Core Components

1. **FastAPI Application**: The main entry point and REST API controller
2. **Risk Calculation Engine**: Algorithms to compute risk scores based on multiple factors
3. **SQLite Database**: Persistent storage for risk evaluations
4. **ORM Layer**: SQLAlchemy for database interactions
5. **Testing Framework**: Pytest for unit and integration tests

### Directory Structure

```
risk-engine/
├── app/
│   ├── __init__.py
│   ├── main.py           # Application entry point
│   ├── database.py       # Database connection and session management
│   ├── models.py         # SQLAlchemy data models
│   ├── routes.py         # API route definitions
│   └── logic/            # Business logic
│       ├── __init__.py
│       ├── risk_calculator.py  # Enhanced risk calculation algorithms
│       └── risk_scoring.py     # Basic risk scoring functionality
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Test fixtures and configuration
│   ├── test_api.py       # API endpoint tests
│   ├── test_logic.py     # Business logic tests
│   └── test_simple.py    # Basic functionality tests
└── venv/                 # Virtual environment
```

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /api/health`

Provides system health status including database connectivity.

**Example Response**:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 2. Risk Evaluation

**Endpoint**: `POST /api/evaluate`

Evaluates the risk of a business based on provided metrics.

**Request Body**:
```json
{
  "user_id": "string",
  "companyName": "string",
  "debtToEquity": 0.0,
  "netProfit": 0.0,
  "negativeNewsScore": 0.0,
  "latePaymentsRate": 0.0,
  "sector": "string"
}
```

**Fields Description**:
- `user_id`: Unique identifier for the user requesting the evaluation
- `companyName`: Name of the company being evaluated
- `debtToEquity`: Debt-to-equity ratio, measuring financial leverage
- `netProfit`: Net profit in local currency
- `negativeNewsScore`: Score from 0-1 representing negative press coverage (higher is worse)
- `latePaymentsRate`: Percentage of late payments as a decimal (0-1)
- `sector`: Industry sector (e.g., "technology", "healthcare", "finance")

**Example Response**:
```json
{
  "evaluation_id": 123,
  "score": 75.5,
  "recommendation": "Medium Risk",
  "explanations": [
    "High debt-to-equity ratio increases financial risk",
    "Negative press coverage may impact business reputation",
    "Industry sector has moderate baseline risk"
  ],
  "recommendations": [
    "Quarterly financial health monitoring recommended",
    "Develop action plan for identified risk areas",
    "Evaluate competitive positioning in volatile market"
  ]
}
```

### 3. Get Evaluation by ID

**Endpoint**: `GET /api/evaluations/{evaluation_id}`

Retrieves a specific risk evaluation by its ID.

**Example Response**:
```json
{
  "id": 123,
  "user_id": "user123",
  "company_name": "Tech Solutions Inc",
  "score": 75.5,
  "recommendation": "Medium Risk",
  "created_at": "2023-08-15T14:30:00",
  "risk_factors": {
    "debtToEquity": 2.5,
    "netProfit": -10000,
    "negativeNewsScore": 0.4,
    "latePaymentsRate": 0.15,
    "sector": "technology"
  }
}
```

### 4. Get Company Evaluations

**Endpoint**: `GET /api/evaluations/company/{company_name}`

Retrieves all risk evaluations for a specific company.

**Example Response**:
```json
[
  {
    "id": 123,
    "user_id": "user123",
    "company_name": "Tech Solutions Inc",
    "score": 75.5,
    "recommendation": "Medium Risk",
    "created_at": "2023-08-15T14:30:00"
  },
  {
    "id": 124,
    "user_id": "user456",
    "company_name": "Tech Solutions Inc",
    "score": 68.2,
    "recommendation": "Medium Risk",
    "created_at": "2023-08-20T09:15:00"
  }
]
```

## Risk Calculation Logic

The risk engine calculates scores based on the following factors:

1. **Financial Health**
   - Debt-to-equity ratio: Higher ratios indicate higher financial risk
   - Net profit: Negative profits increase risk score

2. **Operational Performance**
   - Late payments rate: Higher rates indicate cash flow issues or poor financial management

3. **External Factors**
   - Negative news coverage: Higher scores indicate reputational risk
   - Industry sector: Different baseline risks based on sector volatility

### Scoring Algorithm

The risk score is calculated as a weighted sum of individual risk factors, normalized to a 0-100 scale:

```
Base Score = (w₁ × debt_to_equity_factor + 
              w₂ × net_profit_factor + 
              w₃ × negative_news_factor + 
              w₄ × late_payments_factor) / sum(weights)
              
Final Score = Base Score × sector_adjustment
```

Where:
- w₁, w₂, w₃, w₄ are the weights assigned to each factor
- sector_adjustment is a multiplier based on the industry sector

### Risk Classifications

- **Low Risk** (0-40): Minimal financial and operational concerns
- **Medium Risk** (41-70): Some concerning factors that should be monitored
- **High Risk** (71-100): Significant risk factors requiring immediate attention

### Risk Recommendations

For each risk evaluation, the system generates actionable recommendations based on the risk level, score, and industry sector. These recommendations are designed to help businesses address their specific risk factors.

#### High Risk Recommendations

For high-risk companies (score 71-100), recommendations typically include:
- Comprehensive financial review
- Debt reduction strategies
- Improved accounts receivable policies
- Sector-specific remediation strategies
- External financial expertise for severe cases (score > 85)

#### Medium Risk Recommendations

For medium-risk companies (score 41-70), recommendations typically include:
- Quarterly financial monitoring
- Targeted action plan for risk areas
- Industry-specific competitive analysis

#### Low Risk Recommendations

For low-risk companies (score 0-40), recommendations typically include:
- Maintaining current financial practices
- Annual risk reassessment

## Database Schema

The system uses SQLite with the following schema:

### RiskEvaluation Table

| Column         | Type      | Description                           |
|----------------|-----------|---------------------------------------|
| id             | Integer   | Primary key                           |
| user_id        | String    | ID of the user requesting evaluation  |
| company_name   | String    | Name of the evaluated company         |
| debt_to_equity | Float     | Debt-to-equity ratio                  |
| net_profit     | Float     | Net profit                            |
| negative_news  | Float     | Negative news score (0-1)             |
| late_payments  | Float     | Late payments rate (0-1)              |
| sector         | String    | Industry sector                       |
| score          | Float     | Calculated risk score                 |
| recommendation | String    | Risk classification                   |
| created_at     | DateTime  | Timestamp of evaluation               |

## Setup and Deployment

### Prerequisites

- Python 3.9+
- SQLite
- pip (Python package manager)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/risk-engine.git
cd risk-engine
```

2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
cd risk-engine
python -m app.main
```

The API will be available at `http://localhost:8000`

### Running Tests

```bash
cd risk-engine
python -m pytest tests -v
```

## Security Considerations

- The API uses input validation to prevent malicious data
- Database queries use parameterized statements to prevent SQL injection
- Error handling is designed to avoid leaking sensitive information

## Performance Characteristics

- The API is designed to handle multiple concurrent requests
- Risk calculations are optimized for performance
- Database queries are indexed for fast retrieval

## Future Enhancements

1. **Machine Learning Integration**: Implement predictive models for more accurate risk assessment
2. **Additional Risk Factors**: Incorporate market trends, economic indicators, and geopolitical factors
3. **Real-time Monitoring**: Add capabilities for continuous risk monitoring with alerts
4. **Multi-tenant Support**: Enhanced isolation for different organizations
5. **Advanced Analytics**: Risk trend analysis and industry benchmarking
6. **Custom Risk Models**: Allow users to define custom risk calculation models 
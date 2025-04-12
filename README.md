# Risk Engine

A FastAPI-based risk engine for evaluating and managing business risks using advanced financial metrics and sector-specific insights.

> 📑 **[View Detailed Documentation](DOCUMENTATION.md)** for a comprehensive technical overview of the Risk Engine, including system architecture, API specifications, risk calculation logic, and more.
> 
> 🔌 **[API Guide with Examples](API_GUIDE.md)** for practical usage examples and integration patterns.

## Features

- **Advanced Risk Analysis**: Calculate risk scores using weighted financial and operational metrics
- **Sector-Specific Assessments**: Customize risk evaluations based on industry characteristics
- **Actionable Recommendations**: Receive tailored business recommendations based on risk profile
- **Historical Tracking**: Store and retrieve past evaluations to track risk trends
- **Comprehensive Explanations**: Understand the factors contributing to risk scores
- **REST API**: Industry-standard API for easy integration with existing systems
- **SQLite/PostgreSQL Support**: Choose your preferred database technology

## Risk Factors Analyzed

| Category | Factors |
|----------|---------|
| **Financial Health** | Debt-to-equity ratio, Net profit |
| **Operational Efficiency** | Late payments rate |
| **External Conditions** | Negative news coverage, Industry sector volatility |

## Risk Classification

| Score Range | Classification | Description |
|-------------|----------------|-------------|
| 0-40 | Low Risk | Minimal financial and operational concerns |
| 41-70 | Medium Risk | Some concerning factors that should be monitored |
| 71-100 | High Risk | Significant risk factors requiring immediate attention |

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Configuration

The application uses SQLite by default, which requires no additional setup.

By default, a SQLite database file `risk_engine.db` will be created in the application directory.

#### Optional: Using PostgreSQL Instead

If you prefer to use PostgreSQL:

1. Uncomment the `psycopg2-binary` line in `requirements.txt` and run `pip install -r requirements.txt` again
2. Set the `DATABASE_URL` environment variable:

```bash
# Windows
set DATABASE_URL=postgresql://postgres:secret@localhost:5432/risk_engine_db

# Linux/macOS
export DATABASE_URL=postgresql://postgres:secret@localhost:5432/risk_engine_db
```

### 3. Run the Application

```bash
cd risk-engine
python -m app.main
```

The application will start on port 8000 and create any necessary database tables automatically.

## API Endpoints

- `POST /api/evaluate`: Evaluate risk for a company and get recommendations
- `GET /api/evaluations/{evaluation_id}`: Retrieve a specific risk evaluation
- `GET /api/evaluations/company/{company_name}`: Retrieve all evaluations for a company
- `GET /api/health`: Check API and database health

## Running Tests

```bash
cd risk-engine
python -m pytest -v tests/
```

The tests automatically use an in-memory SQLite database, so no additional setup is required.

## Example Request & Response

**Request:**
```bash
curl -X POST http://localhost:8000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "companyName": "Acme Corp",
    "debtToEquity": 2.5,
    "netProfit": -1000,
    "negativeNewsScore": 0.8,
    "latePaymentsRate": 0.2,
    "sector": "technology"
  }'
```

**Response:**
```json
{
  "evaluation_id": 1,
  "score": 76.8,
  "recommendation": "High Risk",
  "explanations": [
    "High debt-to-equity ratio increases financial risk",
    "Negative net profit shows concerning financial performance",
    "High negative news coverage may impact business reputation",
    "Elevated late payments rate may indicate cash flow issues",
    "Technology sector has moderate baseline risk"
  ],
  "recommendations": [
    "Conduct immediate comprehensive financial review",
    "Develop debt reduction strategy",
    "Implement stricter accounts receivable policies",
    "Evaluate competitive positioning in volatile market"
  ]
}
```

## License

This project is available under the MIT License. See the LICENSE file for details. 
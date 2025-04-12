# Risk Engine API Guide

This guide provides practical examples of using the Risk Engine API for evaluating business risks.

## Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check system health |
| `/api/evaluate` | POST | Evaluate business risk |
| `/api/evaluations/{id}` | GET | Get evaluation by ID |
| `/api/evaluations/company/{name}` | GET | Get evaluations by company name |

## Authentication

The API currently uses open access without authentication. For production use, implement appropriate authentication.

## Examples

### Checking API Health

**Request:**
```bash
curl -X GET http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Evaluating Business Risk

**Request:**
```bash
curl -X POST http://localhost:8000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "companyName": "Tech Innovations Inc",
    "debtToEquity": 1.8,
    "netProfit": 250000,
    "negativeNewsScore": 0.2,
    "latePaymentsRate": 0.05,
    "sector": "technology"
  }'
```

**Response:**
```json
{
  "evaluation_id": 42,
  "score": 35.2,
  "recommendation": "Low Risk",
  "explanations": [
    "Debt-to-equity ratio is within acceptable range",
    "Positive net profit indicates good financial health",
    "Low negative news coverage",
    "Low rate of late payments suggests good cash flow management",
    "Technology sector has moderate baseline risk"
  ],
  "recommendations": [
    "Maintain current financial practices",
    "Annual risk reassessment recommended"
  ]
}
```

### High Risk Example

**Request:**
```bash
curl -X POST http://localhost:8000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user456",
    "companyName": "Struggling Ventures",
    "debtToEquity": 4.2,
    "netProfit": -350000,
    "negativeNewsScore": 0.75,
    "latePaymentsRate": 0.3,
    "sector": "retail"
  }'
```

**Response:**
```json
{
  "evaluation_id": 43,
  "score": 82.7,
  "recommendation": "High Risk",
  "explanations": [
    "Very high debt-to-equity ratio indicates significant financial leverage",
    "Negative net profit shows concerning financial performance",
    "High negative news coverage may impact business reputation",
    "High rate of late payments suggests cash flow problems",
    "Retail sector faces additional challenges in current market conditions"
  ],
  "recommendations": [
    "Conduct immediate comprehensive financial review",
    "Develop debt reduction strategy",
    "Implement stricter accounts receivable policies",
    "Review inventory management to improve cash flow"
  ]
}
```

### Retrieving a Specific Evaluation

**Request:**
```bash
curl -X GET http://localhost:8000/api/evaluations/42
```

**Response:**
```json
{
  "id": 42,
  "user_id": "user123",
  "company_name": "Tech Innovations Inc",
  "score": 35.2,
  "recommendation": "Low Risk",
  "created_at": "2023-08-15T14:30:00",
  "risk_factors": {
    "debtToEquity": 1.8,
    "netProfit": 250000,
    "negativeNewsScore": 0.2,
    "latePaymentsRate": 0.05,
    "sector": "technology"
  },
  "recommendations": [
    "Maintain current financial practices",
    "Annual risk reassessment recommended"
  ]
}
```

### Retrieving All Evaluations for a Company

**Request:**
```bash
curl -X GET "http://localhost:8000/api/evaluations/company/Tech%20Innovations%20Inc"
```

**Response:**
```json
[
  {
    "id": 42,
    "user_id": "user123",
    "company_name": "Tech Innovations Inc",
    "score": 35.2,
    "recommendation": "Low Risk",
    "created_at": "2023-08-15T14:30:00"
  },
  {
    "id": 50,
    "user_id": "user789",
    "company_name": "Tech Innovations Inc",
    "score": 38.1,
    "recommendation": "Low Risk",
    "created_at": "2023-09-20T10:15:00"
  }
]
```

## Risk Score Interpretation

| Score Range | Risk Level | Interpretation |
|-------------|------------|----------------|
| 0-40 | Low Risk | Minimal financial and operational concerns |
| 41-70 | Medium Risk | Some concerning factors that should be monitored |
| 71-100 | High Risk | Significant risk factors requiring immediate attention |

## Common Errors

| Status Code | Meaning | Possible Cause |
|-------------|---------|----------------|
| 404 | Not Found | Evaluation ID or company name doesn't exist |
| 422 | Validation Error | Missing or invalid input parameters |
| 500 | Server Error | Database connection issue or internal processing error |

## Using with Python

Here's a simple Python script to interact with the API:

```python
import requests
import json

# Base URL for the API
base_url = "http://localhost:8000"

# Evaluate a company
def evaluate_company(company_data):
    response = requests.post(
        f"{base_url}/api/evaluate",
        headers={"Content-Type": "application/json"},
        data=json.dumps(company_data)
    )
    return response.json()

# Get evaluation by ID
def get_evaluation(evaluation_id):
    response = requests.get(f"{base_url}/api/evaluations/{evaluation_id}")
    return response.json()

# Example usage
company_data = {
    "user_id": "user123",
    "companyName": "Sample Corp",
    "debtToEquity": 2.1,
    "netProfit": 125000,
    "negativeNewsScore": 0.3,
    "latePaymentsRate": 0.1,
    "sector": "finance"
}

# Evaluate the company
result = evaluate_company(company_data)
print(f"Risk Score: {result['score']}")
print(f"Recommendation: {result['recommendation']}")

# Get the detailed evaluation
if 'evaluation_id' in result:
    details = get_evaluation(result['evaluation_id'])
    print(f"Created at: {details['created_at']}")
```

## Webhook Integration

To receive risk evaluation results via webhook:

1. Add a `webhook_url` parameter to your evaluation request
2. The system will POST the evaluation results to the provided URL
3. Ensure your webhook endpoint can process JSON payloads 
# Pressure Performance API
A cricket analytics engine that evaluates batting performance under pressure versus baseline conditions, providing a normalized score (0-100) and actionable verdict.

## API Objective
Measures how reliably a batsman performs in high-pressure situations (death overs, high required run rates, low wicket remaining, or after a dismissal) compared to their baseline performance in non-pressure scenarios.

## Endpoint

POST /pressure-performance
Input Schema
```json
{
  "player_id": "string (required, min 1 char)",
  "match_id": "string (required, min 1 char)",
  "innings_id": "string (required, min 1 char)",
  "innings_data": [
    {
      "runs": "integer (required, ≥ 0)",
      "balls": "integer (required, > 0)",
      "out": "boolean (required)",
      "phase": "string (required, enum: 'powerplay' | 'middle' | 'death')",
      "rrr": "float (required, ≥ 0)",
      "crr": "float (required, ≥ 0)",
      "wkts": "integer (required, 0-10)"
    }
  ]
}
Example Request
json
{
  "player_id": "PLAYER_001",
  "match_id": "MATCH_2024_01",
  "innings_id": "INN_001",
  "innings_data": [
    {
      "runs": 45,
      "balls": 30,
      "out": false,
      "phase": "powerplay",
      "rrr": 7.5,
      "crr": 9.0,
      "wkts": 1
    },
    {
      "runs": 28,
      "balls": 22,
      "out": true,
      "phase": "death",
      "rrr": 12.0,
      "crr": 8.5,
      "wkts": 7
    },
    {
      "runs": 52,
      "balls": 38,
      "out": false,
      "phase": "middle",
      "rrr": 8.2,
      "crr": 8.2,
      "wkts": 3
    }
  ]
}
Output Schema
json
{
  "meta": {
    "api": "string",
    "version": "string",
    "status": "string"
  },
  "data": {
    "pressure_intensity": "float (0-1)",
    "pressure_performance": "float",
    "baseline_performance": "float",
    "relative_ratio": "float",
    "risk_penalty": "float (0-1)",
    "final_score": "float (0-100)",
    "pressure_innings_count": "integer",
    "baseline_innings_count": "integer",
    "verdict": "string",
    "summary": "string"
  },
  "errors": "object or null"
}
Verdict Values
> 75 → "Reliable Under Pressure"

50 - 75 → "Moderate Under Pressure"

< 50 → "Weak Under Pressure"

Example Response
json
{
  "meta": {
    "api": "pressure-performance",
    "version": "2.2",
    "status": "success"
  },
  "data": {
    "pressure_intensity": 0.78,
    "pressure_performance": 118.42,
    "baseline_performance": 135.6,
    "relative_ratio": 0.87,
    "risk_penalty": 0.33,
    "final_score": 67.32,
    "pressure_innings_count": 1,
    "baseline_innings_count": 2,
    "verdict": "Moderate Under Pressure",
    "summary": "Player shows moderate stability under pressure but has occasional breakdowns."
  },
  "errors": null
} 
## Validation Errors
Empty Innings Data
```json
{
  "detail": "innings_data cannot be empty"
}
Status: 400 Bad Request

No Pressure Situations Found
json
{
  "detail": "No pressure situations found in innings_data"
}
Status: 400 Bad Request

No Baseline Innings Found
json
{
  "detail": "No baseline (non-pressure) innings found — cannot compute relative ratio"
}
Status: 400 Bad Request

Empty ID Fields
json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "player_id"],
      "msg": "Value error, ID cannot be empty",
      "input": ""
    }
  ]
}
Status: 422 Unprocessable Entity

Integration Usage
python
import requests

url = "http://your-api.com/pressure-performance"

payload = {
    "player_id": "PLAYER_001",
    "match_id": "MATCH_2024_01",
    "innings_id": "INN_001",
    "innings_data": [
        {
            "runs": 45,
            "balls": 30,
            "out": False,
            "phase": "powerplay",
            "rrr": 7.5,
            "crr": 9.0,
            "wkts": 1
        }
    ]
}
```json
response = requests.post(url, json=payload)
print(response.json())
javascript
// JavaScript / Node.js
const response = await fetch("http://your-api.com/pressure-performance", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload)
});
const data = await response.json();
curl
curl -X POST http://your-api.com/pressure-performance \
  -H "Content-Type: application/json" \
  -d '{
    "player_id": "PLAYER_001",
    "match_id": "MATCH_2024_01",
    "innings_id": "INN_001",
    "innings_data": []
  }'
 ## Conclusion
The Pressure Performance API provides a data-driven approach to evaluating a batsman's temperament and reliability in critical match situations. By combining multiple pressure indicators — match phase, required run rate, wickets fallen, and dismissal events — the engine intelligently segments performance data into pressure and baseline categories. The weighted scoring model, risk penalty adjustment, and sigmoid normalization produce a final 0-100 score that is both interpretable and actionable for coaches, analysts, and selectors. This enables evidence-based decisions on player selection, batting order positioning, and situational match strategy.
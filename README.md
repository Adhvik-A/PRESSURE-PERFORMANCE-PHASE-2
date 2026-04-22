# Pressure Performance API
# Overview

The Pressure Performance API is a cricket analytics engine that evaluates a batter’s performance under pressure situations compared to baseline conditions. It analyzes innings-level data to determine consistency, clutch ability, and failure risk.

# Objective

To measure how well a player performs under high-pressure match conditions using:

Pressure Intensity
Pressure Performance
Baseline Performance
Relative Ratio
Risk Penalty
Final Performance Score

#  Architecture
pres.py        → FastAPI server (routes + CORS)
services.py    → Business logic pipeline
utils.py       → Core mathematical engine
schemas.py     → Request/Response validation

# Features
 Pressure vs Baseline analysis
 Dynamic pressure classification
 Risk penalty detection (failure under pressure)
 Normalized performance scoring (0–100)
 Human-readable performance summary
 Fully modular architecture

#  API Endpoints
🔹 1. Health Check
GET /health

Response:

{
  "status": "ok",
  "service": "pressure-api"
}
🔹 2. API Description
GET /description
🔹 3. Pressure Performance Analysis
POST /pressure-performance

# Input Schema
{
  "innings_data": [
    {
      "runs": 50,
      "balls": 30,
      "out": true,
      "phase": "death",
      "rrr": 10.5,
      "crr": 8.2,
      "wkts": 6
    }
  ]
}
# Output Schema
{
  "pressure_intensity": 0.85,
  "pressure_performance": 110.25,
  "baseline_performance": 82.40,
  "relative_ratio": 1.15,
  "risk_penalty": 0.32,
  "final_score": 78.60,
  "verdict": "Reliable Under Pressure",
  "summary": "Player performs consistently under extreme pressure with strong control and execution."
}

# Core Logic
🔹 Pressure Calculation

Combines:

Required Run Rate vs Current Run Rate
Wicket pressure
Match phase weight
🔹 Pressure Performance

Measures batting efficiency only in high-pressure innings.

🔹 Baseline Performance

Measures performance in non-pressure situations (or fallback estimation if missing).

🔹 Risk Penalty

Penalizes:

low scoring under pressure
frequent dismissals in critical situations
🔹 Final Score

Weighted combination of:

pressure performance × intensity × relative ratio × risk adjustment

Normalized to 0–100 scale.

# Verdict System
Score Range	Verdict
75 – 100	Reliable Under Pressure
50 – 75	Moderate Under Pressure
0 – 50	Weak Under Pressure

# Example Test Case
# Input
{
  "innings_data": [
    {
      "runs": 82,
      "balls": 46,
      "out": false,
      "phase": "death",
      "rrr": 11.8,
      "crr": 8.5,
      "wkts": 7
    },
    {
      "runs": 18,
      "balls": 12,
      "out": true,
      "phase": "death",
      "rrr": 12.5,
      "crr": 7.9,
      "wkts": 9
    }
  ]
}
# Output
{
  "pressure_intensity": 1,
  "pressure_performance": 86.21,
  "baseline_performance": 60.34,
  "relative_ratio": 1.23,
  "risk_penalty": 0.5,
  "final_score": 95.08,
  "verdict": "Reliable Under Pressure",
  "summary": "Player performs consistently under extreme pressure with strong control and execution."
}

# Project Structure
project/
│
├── pres.py          # FastAPI app
├── services.py      # Core pipeline logic
├── utils.py         # Math engine
├── schemas.py       # Pydantic models
└── README.md

# Key Highlights
Fully modular design (easy to extend to ML models)
Handles missing baseline scenarios
Built for cricket analytics & performance scouting
Production-ready FastAPI structure

# Future Improvements
ML-based adaptive weighting system
React dashboard for live visualization
Real-time match simulation engine
Player comparison system (A vs B)
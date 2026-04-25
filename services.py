from fastapi import HTTPException
from utils import (
    pressure_performance,
    baseline_performance,
    risk_penalty,
    calculate_pressure,
    normalize_score,
    summary_gen, 
)


WEIGHTS = {
    "run_rate": 0.5,
    "wickets": 0.3,
    "phase": 0.2
}


def process_pressure_data(payload):

    if not payload.innings_data:
        raise HTTPException(status_code=400, detail="innings_data cannot be empty")

    innings_data = [i.dict() for i in payload.innings_data]

    pressure_innings = []
    baseline_innings = []

    # =========================================================
    # SMART SPLIT LOGIC
    # =========================================================
    for i in innings_data:

        score = calculate_pressure(i, WEIGHTS)
        enriched = {**i, "pressure_score": score}

        is_pressure = (
            i["phase"] == "death" or
            i["rrr"] > 10 or
            i["wkts"] >= 7 or
            i["out"] is True
        )

        if is_pressure:
            pressure_innings.append(enriched)
        else:
            baseline_innings.append(enriched)

    # =========================================================
    # VALIDATION — no silent fallbacks
    # =========================================================
    if len(pressure_innings) == 0:
        raise HTTPException(status_code=400, detail="No pressure situations found in innings_data")

    if len(baseline_innings) == 0:
        raise HTTPException(status_code=400, detail="No baseline (non-pressure) innings found — cannot compute relative ratio")

    # =========================================================
    # METRICS
    # =========================================================
    pressure_perf = pressure_performance(pressure_innings)
    base_perf = baseline_performance(baseline_innings, pressure_perf)

    pressure_intensity = sum(
        i["pressure_score"] for i in pressure_innings
    ) / len(pressure_innings)

    relative_ratio = pressure_perf / base_perf if base_perf > 0 else 0
    risk = risk_penalty(pressure_innings)

    # =========================================================
    # SCORE ENGINE
    # =========================================================
    raw_score = (
        relative_ratio *
        pressure_perf *
        pressure_intensity *
        (1 - risk)
    )

    final_score = min(100, normalize_score(raw_score))

    # =========================================================
    # VERDICT
    # =========================================================
    if final_score > 75:
        verdict = "Reliable Under Pressure"
    elif final_score > 50:
        verdict = "Moderate Under Pressure"
    else:
        verdict = "Weak Under Pressure"

  

    # =========================================================
    # RETURN RAW DATA (WRAPPER ADDED IN ROUTE)
    # =========================================================
    return {
        "pressure_intensity": round(pressure_intensity, 2),
        "pressure_performance": round(pressure_perf, 2),
        "baseline_performance": round(base_perf, 2),
        "relative_ratio": round(relative_ratio, 2),
        "risk_penalty": round(risk, 2),
        "final_score": round(final_score, 2),
        "pressure_innings_count": len(pressure_innings),
        "baseline_innings_count": len(baseline_innings),
        "verdict": verdict,
        "summary": summary_gen(final_score)
    }
from utils import (
    split_innings,
    pressure_performance,
    baseline_performance,
    risk_penalty,
    calculate_pressure,
    normalize_score,
    generate_summary
)


WEIGHTS = {
    "run_rate": 0.5,
    "wickets": 0.3,
    "phase": 0.2
}


def process_pressure_data(payload):

    innings_data = [i.dict() for i in payload.innings_data]

    # =============================
    # SPLIT
    # =============================
    pressure_innings, baseline_innings = split_innings(innings_data, WEIGHTS)

    if len(pressure_innings) == 0:
        return {
            "pressure_intensity": 0,
            "pressure_performance": 0,
            "baseline_performance": 0,
            "relative_ratio": 0,
            "risk_penalty": 0,
            "final_score": 0,
            "verdict": "No Pressure Situations Detected",
            "summary": "Insufficient pressure data for evaluation."
        }

    # =============================
    # PRESSURE STATS
    # =============================
    pressure_perf = pressure_performance(pressure_innings)

    # intensity
    pressure_intensity = sum(
        calculate_pressure(i, WEIGHTS) for i in pressure_innings
    ) / len(pressure_innings)

    # =============================
    # BASELINE
    # =============================
    base_perf = baseline_performance(baseline_innings, pressure_perf)

    # =============================
    # RATIOS
    # =============================
    relative_ratio = pressure_perf / (base_perf + 10)
    risk = risk_penalty(pressure_innings)

    # =============================
    # SCORE
    # =============================
    raw_score = (
        relative_ratio *
        pressure_perf *
        pressure_intensity *
        (1 - 0.5 * risk)
    )

    final_score = min(100, normalize_score(raw_score))

    summary = generate_summary(final_score)

    verdict = (
        "Reliable Under Pressure" if final_score > 75 else
        "Moderate Under Pressure" if final_score > 50 else
        "Weak Under Pressure"
    )

    return {
        "pressure_intensity": round(pressure_intensity, 2),
        "pressure_performance": round(pressure_perf, 2),
        "baseline_performance": round(base_perf, 2),
        "relative_ratio": round(relative_ratio, 2),
        "risk_penalty": round(risk, 2),
        "final_score": round(final_score, 2),
        "verdict": verdict,
        "summary": summary
    }
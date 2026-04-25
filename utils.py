import math


def get_phase_factor(phase: str) -> float:
    if phase == "powerplay":
        return 0.3
    elif phase == "middle":
        return 0.6
    return 1.0


def calculate_pressure(innings, weights):
    rrr_ratio = innings["rrr"] / max(innings["crr"], 0.1)
    wickets_pressure = innings["wkts"] / 10
    phase_pressure = get_phase_factor(innings["phase"])

    return min(1, (
        weights["run_rate"] * rrr_ratio +
        weights["wickets"] * wickets_pressure +
        weights["phase"] * phase_pressure
    ))


# =============================
# PRESSURE SPLIT
# =============================
def split_innings(innings_data, weights):
    pressure = []
    baseline = []

    for inn in innings_data:
        p_val = calculate_pressure(inn, weights)
        if p_val >= 0.65:
            pressure.append(inn)
        else:
            baseline.append(inn)

    return pressure, baseline


# =============================
# PRESSURE PERFORMANCE
# =============================
def pressure_performance(pressure_innings):
    runs = sum(i["runs"] for i in pressure_innings)
    balls = sum(i["balls"] for i in pressure_innings)
    outs = sum(i["out"] for i in pressure_innings)

    return (runs / max(balls, 1)) * 100 * (1 - outs / len(pressure_innings))


# =============================
# BASELINE PERFORMANCE
# =============================
def baseline_performance(baseline_innings, fallback_from_pressure):
    if len(baseline_innings) == 0:
        return fallback_from_pressure * 0.7

    runs = sum(i["runs"] for i in baseline_innings)
    balls = sum(i["balls"] for i in baseline_innings)
    outs = sum(i["out"] for i in baseline_innings)

    return (runs / max(balls, 1)) * 100 * (1 - outs / len(baseline_innings))


# =============================
# RISK PENALTY
# =============================
def risk_penalty(pressure_innings):
    failures = 0

    for inn in pressure_innings:
        expected = inn["balls"] * 1.2
        if inn["runs"] < 0.85 * expected or inn["runs"] < 20:
            failures += 1

    return failures / max(len(pressure_innings), 1)


# =============================
# SUMMARY GENERATOR
# =============================
def summary_gen(score):
    if score > 75:
        return "Player performs consistently under extreme pressure with strong control and execution."
    elif score > 50:
        return "Player shows moderate stability under pressure but has occasional breakdowns."
    else:
        return "Player struggles under high-pressure situations and lacks consistency in critical moments."


def normalize_score(raw_score: float):
    k = 0.05
    midpoint = 20
    return round(100 / (1 + math.exp(-k * (raw_score - midpoint))), 2)
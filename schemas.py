from pydantic import BaseModel
from typing import List


class Innings(BaseModel):
    runs: int
    balls: int
    out: bool
    phase: str
    rrr: float
    crr: float
    wkts: int


class PressureRequest(BaseModel):
    innings_data: List[Innings]


class PressureResponse(BaseModel):
    pressure_intensity: float
    pressure_performance: float
    baseline_performance: float
    relative_ratio: float
    risk_penalty: float
    final_score: float
    verdict: str
    summary:str
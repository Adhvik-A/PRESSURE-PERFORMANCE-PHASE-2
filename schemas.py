from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import List, Any, Optional, Literal


# =========================================================
# ENUMS
# =========================================================
class PhaseType(str, Enum):
    powerplay = "powerplay"
    middle = "middle"
    death = "death"


# =========================================================
# INNINGS MODEL
# =========================================================
class InningsData(BaseModel):
    runs: int = Field(..., ge=0)
    balls: int = Field(..., gt=0)
    out: bool
    phase: Literal["powerplay", "middle", "death"]
    rrr: float = Field(..., ge=0)
    crr: float = Field(..., ge=0)
    wkts: int = Field(..., ge=0, le=10)


# =========================================================
# REQUEST MODEL
# =========================================================
class PressureRequest(BaseModel):

    player_id: str = Field(..., min_length=1)
    match_id: str = Field(..., min_length=1)
    innings_id: str = Field(..., min_length=1)

    innings_data: List[InningsData]


    @field_validator("player_id", "match_id", "innings_id")
    @classmethod
    def validate_ids(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("ID cannot be empty")
        return v


# =========================================================
# RESPONSE MODEL
# =========================================================
class PressureResponse(BaseModel):

    pressure_intensity: float
    pressure_performance: float
    baseline_performance: float
    relative_ratio: float
    risk_penalty: float
    final_score: float

    pressure_innings_count: int
    baseline_innings_count: int

    verdict: str
    summary: str


# =========================================================
# STANDARD API WRAPPER
# =========================================================
class Meta(BaseModel):
    api: str
    version: str = "1.0"
    status: str


class StandardResponse(BaseModel):
    meta: Meta
    data: Any
    errors: Optional[Any] = None
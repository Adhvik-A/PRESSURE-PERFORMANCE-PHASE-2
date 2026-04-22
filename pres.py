from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import PressureRequest, PressureResponse
from services import process_pressure_data

app = FastAPI(
    title="Pressure Performance API",
    description="Cricket analytics engine for pressure vs baseline evaluation",
    version="2.2"
)

# =============================
# CORS
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================
# HEALTH CHECK
# =============================
@app.get("/health")
def health():
    return {"status": "ok", "service": "pressure-api"}


# =============================
# DESCRIPTION
# =============================
@app.get("/description")
def description():
    return {
        "name": "Pressure Performance API",
        "version": "2.2",
        "objective": "Measures batting performance under pressure vs baseline",
        "status": "active"
    }


# =============================
# MAIN ENDPOINT
# =============================
@app.post("/pressure-performance", response_model=PressureResponse)
def pressure_performance(payload: PressureRequest):
    return process_pressure_data(payload)


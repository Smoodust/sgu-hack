from typing import Annotated
from fastapi import BackgroundTasks, FastAPI, File, HTTPException

from prometheus_fastapi_instrumentator import Instrumentator

import numpy as np
import pandas as pd
import random

from models.network import model
from monitoring_app import metrics_app, calculate_drift, DRIFT_SCORE


df = pd.read_parquet("./features.parquet")
shops = [col for col in df.columns if col not in ["client_id", "timestamp"]]

app = FastAPI()

app.mount("/metrics", metrics_app)
Instrumentator().instrument(app).expose(app)


@app.get("/predict", status_code=200)
def recomend_cashbacks(client_username: str):
    global model
    if model is None:
        raise HTTPException(status_code=404, detail="No models found")
    
    feature = np.array([random.randint(0, 1) for i in range(50)])

    try:
        recommendations = model(feature)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

    return recommendations


@app.get("/check_drift", status_code=200)
def check_drift():
    user_data = df.copy()

    numeric_cols = user_data.select_dtypes(include=[np.number]).columns
    numeric_data = user_data[numeric_cols]

    noise = np.random.binomial(n=1, p=0.1, size=numeric_data.shape)
    numeric_data = (numeric_data + noise) % 2

    user_data[numeric_cols] = numeric_data

    try:
        metrics = calculate_drift(user_data[numeric_cols])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing drift calculation: {str(e)}"
        )

    return metrics

@app.post("/check_alert", status_code=200)
def check_alert():
    DRIFT_SCORE.set(1)
    return {
        "OH, NO!!!! IT'S DRIFTING~~~"
    }


@app.get("/train")
def retrain_model():
    pass

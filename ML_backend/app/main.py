from typing import List
from fastapi import FastAPI, HTTPException, Query
import requests

from prometheus_fastapi_instrumentator import Instrumentator

import numpy as np
import random

import fasttext

from monitoring_app import metrics_app, calculate_drift, DRIFT_SCORE


app = FastAPI(
    title="ML Log Analysis API",
    description="API for ML Log Analysis",
    version="1.0.0",
    openapi_tags=[{
        "name": "ML Log Analysis",
        "description": "Operations with log files analysis"
    }]
)

app.mount("/metrics", metrics_app)
Instrumentator().instrument(app).expose(app)

classifier_model = fasttext.load_model("./app/models/logs_classifier.bin")


@app.get(
        "/predict_sus_lines", 
        status_code=200,
        summary="Отдает подозрительные строчки"
)
def predict_sus_lines(
    log_url: str = Query(
        ...,
        description="URL логов"
    ), 
    top_k: int = Query(
        5,
        ge=1,
        le=50,
        example=5,
        description="Количество отдаваемых строчек"
    )
) -> List[str]:
    global classifier_model
    if classifier_model is None:
        raise HTTPException(status_code=404, detail="No models found")
    
    try:
        log = requests.get(log_url).text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch log: {str(e)}")
    
    if not log:
        raise HTTPException(status_code=404, detail="No logs found")
    
    lines = log.splitlines()[-500:] 
    predictions = []

    for line in lines:
        if not line.strip():
            continue
            
        try:
            (label,), (prob,) = classifier_model.predict(line.strip(), k=1)
            predictions.append((line, prob))
        except Exception as e:
            continue 

    predictions.sort(key=lambda x: x[1], reverse=True)
    top_sus_lines = [line for line, prob in predictions[:top_k]]
    
    return top_sus_lines


@app.get(
        "/check_drift", 
        status_code=200,
        summary="Проверка модели на дрифт"
)
def check_drift():
    pass

@app.post(
        "/check_alert", 
        status_code=200,
        summary="Проверка алертов Grafana"
)
def check_alert():
    DRIFT_SCORE.set(1)
    return {
        "OH, NO!!!! IT'S DRIFTING~~~"
    }


@app.get("/train")
def retrain_model():
    pass

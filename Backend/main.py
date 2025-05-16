from datetime import datetime
from typing import Annotated

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import BackgroundTasks, FastAPI, File, HTTPException

from prometheus_fastapi_instrumentator import Instrumentator

import numpy as np
import pandas as pd
import random

from starlette.responses import JSONResponse

from models.network import model
from monitoring_app import metrics_app, calculate_drift, DRIFT_SCORE
from pymongo import MongoClient

# Подключение к локальному серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Или с аутентификацией
# client = MongoClient('mongodb://username:password@localhost:27017/')

# Выбор базы данных
db = client['sgu_hack']

# Выбор коллекции (аналог таблицы в SQL)
collection = db['logs']


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

@app.get('/get_logs')
async def get_logs():
    res =  requests.get('')

@app.post("/check_alert", status_code=200)
def check_alert():
    DRIFT_SCORE.set(1)
    return {
        "OH, NO!!!! IT'S DRIFTING~~~"
    }


@app.get("/train")
def retrain_model():
    pass

async def task():
    res = requests.get('https://rdb.altlinux.org/api/export/beehive/ftbfs?branch=sisyphus&arch=i586')
    if res.status_code == 200:
        document = {
            'datetime': datetime.now(),  # Текущая дата и время
            'json': res.json(),  # Произвольные JSON данные
            'is_checked': True,
            'is_worked': False
        }
        collection.insert_one(document)
        return res.json()
    raise HTTPException(
            status_code=500, detail=f"Error with request"
        )



scheduler = BackgroundScheduler()
scheduler.add_job(task, 'interval', minutes=5)  # Интервал в 5 минут
scheduler.start()

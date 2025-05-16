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

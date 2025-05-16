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
from db.db import *

from handlers.handlers import router

URL_PARSE_LOGS = 'https://rdb.altlinux.org/api/export/beehive/ftbfs?branch=sisyphus&arch=x86_64'


# # Задача для загрузки логов из внешнего источника
# async def task():
#     res = requests.get(URL_PARSE_LOGS)
#     if res.status_code == 200:
#         document = {
#             'datetime': datetime.now(),  # Текущая дата и время
#             'json': res.json(),  # Произвольные JSON данные
#             'is_checked': True,
#             'is_worked': False
#         }
#         dbase.new_logs(document)
#         return res.json()
#     raise HTTPException(
#             status_code=500, detail=f"Error with request"
#         )



scheduler = BackgroundScheduler()
scheduler.add_job(parse_logs(URL_PARSE_LOGS), 'cron', hour=5, minute=0)  # Запуск каждый день в 05:00
scheduler.start()



app = FastAPI(
    title="SGU Hackathon 2025",
    description="API для системы мониторинга и анализа логов",
    version="1.0.0"
)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

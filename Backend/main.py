import requests
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException
from datetime import datetime

from starlette.middleware.cors import CORSMiddleware

from db.db import parse_logs
from db.config import URL_PARSE_LOGS
from handlers.swaggerDis import custom_openapi
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
scheduler.add_job(parse_logs, 'cron', args=[URL_PARSE_LOGS], hour=5, minute=0)  # Запуск каждый день в 05:00
scheduler.start()



app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3001",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = lambda: custom_openapi(app)

app.include_router(router)

if __name__ == "__main__":
    parse_logs(URL_PARSE_LOGS)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

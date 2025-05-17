from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db.db import *
from AI.ai import *
import json
import requests
from datetime import datetime

router = APIRouter()


## Хандлер для динаическрй подгрузки логов
@router.get("/logs")
async def get_logs():
    try:
        logs = dbase.get_logs()
        for log in logs:
            log['updated'] = log['updated'].strftime("%Y-%m-%d %H:%M:%S")
            log['tbfs_since'] = log['tbfs_since'].strftime("%Y-%m-%d %H:%M:%S") 
        return JSONResponse(content={"logs":logs}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Хандлер для лога по ID
@router.get("/logs/{id}")
async def get_log(id: str):
    try:
        log = dbase.get_log(id) 
        log['updated'] = log['updated'].strftime("%Y-%m-%d %H:%M:%S")
        log['tbfs_since'] = log['tbfs_since'].strftime("%Y-%m-%d %H:%M:%S")
        return JSONResponse(content={"log":log}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Графики количества неисправленных пакетов за последний месяц
@router.get("/graphs")
async def get_graphs():
    try:
        graphs = dbase.get_graphs()
        return JSONResponse(content={"graphs":graphs['graphs'], "count_logs":graphs['count_logs']}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## График по периоду 
@router.post("/graphs/period")
async def get_graphs_period(period: dict):
    try:
        startDate = datetime.strptime(period["startDate"], "%Y-%m-%d:%H:%M:%S")
        endDate = datetime.strptime(period["endDate"], "%Y-%m-%d:%H:%M:%S")
        graphs = dbase.get_graphs_period(startDate=startDate, endDate=endDate)
        return JSONResponse(content={"graphs":graphs['graphs'], "count_logs":graphs['count_logs']}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## График по пакету 
@router.get("/graphs/package/{package}")
async def get_graphs_package(package: str):
    try:
        graphs = dbase.get_graphs_package(package)
        return JSONResponse(content={"graphs":graphs['graphs'], "count_logs":graphs['count_logs']}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## График по пакету и периоду 
@router.post("/graphs/packageANDperiod")
async def get_graphs_package_period(body: dict):
    try:
        package = body["package"]
        startDate = datetime.strptime(body["startDate"], "%Y-%m-%d:%H:%M:%S")
        endDate = datetime.strptime(body["endDate"], "%Y-%m-%d:%H:%M:%S")
        graphs = dbase.get_graphs_package_period(package=package, startDate=startDate, endDate=endDate)
        return JSONResponse(content={"graphs":graphs['graphs'], "count_logs":graphs['count_logs']}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Хандлер который анализирует лог и возвращает результат
@router.get("/logs/analyze/{id}")
async def analyze_log(id: str):
    try:
        # TODO: Добавить AI Кирилла, которая возвращает подозрительные строки в логе
        log_struct = dbase.get_log(id)
        if log_struct:
            log_url = log_struct['url']
            log = requests.get(log_url).text
            result = ai_parse(log)
            print(result)
            return JSONResponse(content={"result":result, "log": log}, status_code=200)
        else:
            return JSONResponse(content={"result":"Log not found"}, status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
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
        graphs_cluster_array = []
        logs = dbase.get_logs()
        limit = 20
        for log in logs:
            graphs_cluster = dbase.get_graphs_cluster(log['id'])
            if graphs_cluster and len(graphs_cluster) >= 5:
                graphs_cluster_array += [graphs_cluster[1],graphs_cluster[2], graphs_cluster[3], graphs_cluster[4]]
            elif limit > 0:
                request_info = requests.get(f"http://ml_dev:8000/predict_logs_cordinate?log_url={log['url']}")   
                request_info = request_info.json()
                graphs_cluster_array += [request_info['x'], request_info['y'], request_info['cluster']]
                dbase.new_cluster(log['id'], request_info['x'], request_info['y'], request_info['cluster']) 
                limit -= 1
            else:
                break

        return JSONResponse(content={"graphs":graphs['graphs'], "count_logs":graphs['count_logs'], "graphs_cluster":graphs_cluster_array}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## График по периоду 
@router.post("/graphs/period")
async def get_graphs_period(period: dict):
    try:
        startDate = datetime.strptime(period["startDate"], "%Y-%m-%d:%H:%M:%S")
        endDate = datetime.strptime(period["endDate"], "%Y-%m-%d:%H:%M:%S")
        graphs = dbase.get_graphs_period(startDate=startDate, endDate=endDate)
        graphs_cluster_array = []
        logs = dbase.get_logs()
        limit = 20
        for log in logs:
            graphs_cluster = dbase.get_graphs_cluster_period(log['id'], startDate, endDate)
            if graphs_cluster and len(graphs_cluster) >= 5:
                graphs_cluster_array += [graphs_cluster[1],graphs_cluster[2], graphs_cluster[3], graphs_cluster[4]]
            elif limit > 0:
                request_info = requests.get(f"http://ml_dev:8000/predict_logs_cordinate?log_url={log['url']}")   
                request_info = request_info.json()
                graphs_cluster_array += [request_info['x'], request_info['y'], request_info['cluster']]
                dbase.new_cluster(log['id'], request_info['x'], request_info['y'], request_info['cluster'])
                limit -= 1
            else:
                break

        return JSONResponse(content={"graphs":graphs['graphs'], "count_logs":graphs['count_logs'], "graphs_cluster":graphs_cluster_array}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## График по пакету 
@router.get("/graphs/package/{package}")
async def get_graphs_package(package: str):
    try:
        graphs = dbase.get_graphs_package(package)
        graphs_cluster_array = []
        logs = dbase.get_logs()
        limit = 20
        for log in logs:
            graphs_cluster = dbase.get_graphs_cluster_package(log['id'], package)
            if graphs_cluster and len(graphs_cluster) >= 5:  # Проверяем, что в массиве достаточно элементов
                graphs_cluster_array += [graphs_cluster[1], graphs_cluster[2], graphs_cluster[3], graphs_cluster[4]]
            elif limit > 0:
                request_info = requests.get(f"http://ml_dev:8000/predict_logs_cordinate?log_url={log['url']}")   
                request_info = request_info.json()
                graphs_cluster_array += [request_info['x'], request_info['y'], request_info['cluster']]
                dbase.new_cluster(log['id'], request_info['x'], request_info['y'], request_info['cluster'])
                limit -= 1
            else:
                break

        return JSONResponse(content={"graphs":graphs['graphs'], "count_logs":graphs['count_logs'], "graphs_cluster":graphs_cluster_array}, status_code=200)
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
        graphs_cluster_array = []
        logs = dbase.get_logs()
        limit = 20
        for log in logs:
            graphs_cluster = dbase.get_graphs_cluster_package_period(log['id'], package, startDate, endDate)
            if graphs_cluster and len(graphs_cluster) >= 5:
                graphs_cluster_array += [graphs_cluster[1],graphs_cluster[2], graphs_cluster[3], graphs_cluster[4]]
            elif limit > 0:
                request_info = requests.get(f"http://ml_dev:8000/predict_logs_cordinate?log_url={log['url']}")   
                request_info = request_info.json()
                graphs_cluster_array += [request_info['x'], request_info['y'], request_info['cluster']]
                dbase.new_cluster(log['id'], request_info['x'], request_info['y'], request_info['cluster'])
                limit -= 1
            else:
                break

        return JSONResponse(content={"graphs":graphs['graphs'], "count_logs":graphs['count_logs'], "graphs_cluster":graphs_cluster_array}, status_code=200)
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
            info_for_bad_lines = requests.get(f"http://ml_dev:8000/predict_sus_lines?log_url={log_url}&top_k=5")
            info_for_bad_lines = info_for_bad_lines.json()['result']
            result = ai_parse(log)

            print(result)
            return JSONResponse(content={"result":result, "log_url": log_url, "badLines": info_for_bad_lines}, status_code=200)
        else:
            return JSONResponse(content={"result":"Log not found"}, status_code=404)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
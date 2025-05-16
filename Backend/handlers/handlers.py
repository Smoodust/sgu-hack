from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db.db import *

router = APIRouter()


## Хандлер для динаическрй подгрузки логов
@router.get("/logs")
async def get_logs():
    try:
        return JSONResponse(content={"logs":dbase.get_logs()}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Хандлер для лога по ID
@router.get("/logs/{id}")
async def get_log(id: str):
    try:
        return JSONResponse(content={"log":dbase.get_log(id)}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## Графики общие 
@router.get("/graphs")
async def get_graphs():
    try:
        return JSONResponse(content={"graphs":dbase.get_graphs()}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## График по периоду 
@router.post("/graphs/period")
async def get_graphs_period(period: dict):
    try:
        startDate = datetime.strptime(period["startDate"], "%Y-%m-%d:%H:%M:%S")
        endDate = datetime.strptime(period["endDate"], "%Y-%m-%d:%H:%M:%S")
        return JSONResponse(content={"graphs":dbase.get_graphs_period(startDate=startDate, endDate=endDate)}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## График по пакету 
@router.get("/graphs/package/{package}")
async def get_graphs_package(package: str):
    try:
        return JSONResponse(content={"graphs":dbase.get_graphs_package(package)}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## График по пакету и периоду 
@router.post("/graphs/packageANDperiod")
async def get_graphs_package_period(body: dict):
    try:
        package = body["package"]
        startDate = datetime.strptime(body["startDate"], "%Y-%m-%d:%H:%M:%S")
        endDate = datetime.strptime(body["endDate"], "%Y-%m-%d:%H:%M:%S")
        return JSONResponse(content={"graphs":dbase.get_graphs_package_period(package=package, startDate=startDate, endDate=endDate)}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

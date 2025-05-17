import inspect
from fastapi import FastAPI, HTTPException, Query
import requests
from prometheus_fastapi_instrumentator import Instrumentator
import fasttext

from monitoring_app import metrics_app, calculate_sus_lines_drift, SUS_DRIFT_SCORE
from NN_models.network import logs_embedder
from NN_models.kmeans import kmean
from models import SuspiciousLineResponse, CordinateResponse


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

classifier_model = fasttext.load_model("./NN_models/logs_classifier.bin")

def fetch_log_content(log_url: str) -> str:
    """Fetch log content from a given URL with error handling."""
    try:
        response = requests.get(log_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch log: {str(e)}")
    
    log_text = response.text
    if not log_text:
        raise HTTPException(status_code=404, detail="No logs found")
    
    return log_text

@app.get(
    "/predict_logs_cordinate", 
    status_code=200,
    response_model=CordinateResponse,
    summary="Отдает кординаты для лога"
)
def predict_logs_cordinate(
    log_url: str = Query(
        ...,
        description="URL логов"
    )
) -> CordinateResponse:
    global logs_embedder, kmean
    if logs_embedder is None or kmean is None:
        raise HTTPException(status_code=404, detail="No models found")
    
    log = fetch_log_content(log_url)
    
    x, y = logs_embedder(log[-100:]).tolist()
    cluster = kmean(x, y)
    
    return CordinateResponse(x=x, y=y, cluster=cluster)


@app.get(
        "/predict_sus_lines", 
        status_code=200,
        response_model=SuspiciousLineResponse,
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
) -> SuspiciousLineResponse:
    global classifier_model
    if classifier_model is None:
        raise HTTPException(status_code=404, detail="No models found")
    
    try:
        log = requests.get(log_url).text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch log: {str(e)}")
    
    if not log:
        raise HTTPException(status_code=404, detail="No logs found")
    
    lines = log.splitlines()[-100:] 
    predictions = []

    for line_a, line_b in zip(lines[:-1], lines[1:]):
        line = line_a + " " + line_b
        if not line.strip():
            continue
            
        try:
            classifier_model.predict(line.strip(), k=1)
        except Exception as e:
            prob = inspect.trace()[-1][0].f_locals['probs'][0]
            predictions.append((line_a + "\n" + line_b, prob))
    predictions.sort(key=lambda x: x[1], reverse=True)
    calculate_sus_lines_drift(predictions)
    top_sus_lines = [line for line, _ in predictions[:top_k]]
    
    return {
        "result": top_sus_lines
    }

@app.post(
        "/check_alert/sus_lines", 
        status_code=200,
        summary="Проверка алертов Grafana для детекции подозрительных строк"
)
def check_alert():
    SUS_DRIFT_SCORE.set(0.2)
    return {
        "OH, NO!!!! AMOGUS~~~"
    }


@app.get("/train")
def retrain_model():
    pass

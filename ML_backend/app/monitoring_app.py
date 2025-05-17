from prometheus_client import make_asgi_app, Gauge
from typing import List, Tuple, Dict

metrics_app = make_asgi_app()
SUS_DRIFT_SCORE = Gauge("drift_score", "Дрейф модели, детектирующей строки")


def calculate_sus_lines_drift(preds: List[Tuple[str, float]]) -> Dict[str, Tuple[str, float]]:
    if not preds:
        raise ValueError("Input predictions list cannot be empty")
    
    if not all(isinstance(item, tuple) and len(item) == 2 for item in preds):
        raise ValueError("All prediction items must be tuples of (str, float)")
    
    most_suspicious = max(preds, key=lambda x: x[1])
    
    SUS_DRIFT_SCORE.set(most_suspicious[1])
    
    return {
        "drift": most_suspicious
    }
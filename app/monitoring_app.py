from prometheus_client import make_asgi_app, Gauge

import numpy as np
import pandas as pd

metrics_app = make_asgi_app()
DRIFT_SCORE = Gauge("drift_score", "Средний дрейф по магазинам")

current_df = pd.read_parquet("./features.parquet")

def calculate_drift(
        df: pd.DataFrame
):
    numeric_cols = current_df.select_dtypes(include=[np.number]).columns
    current_mean = current_df[numeric_cols].mean(axis=0)
    new_mean = df.mean(axis=0)
    drift = np.abs(current_mean - new_mean).mean()

    DRIFT_SCORE.set(drift)
    
    return {
        "drift": drift
    }
import pandas as pd
from datetime import datetime

def series_to_records(s: pd.Series, key: str = "value") -> list[dict]:
    records = []
    for idx, val in s.dropna().items():
        ts = pd.to_datetime(idx)         # convert idx -> Timestamp (works for strings, timestamps, etc.)
        records.append({"date": ts.strftime("%Y-%m-%d"), key: float(val)})
    return records
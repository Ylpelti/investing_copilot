import pandas as pd
from datetime import datetime

def series_to_records(s: pd.Series, key="value"):
    return [{"date": idx.strftime("%Y-%m-%d"), key: float(val)} for idx, val in s.dropna().items()]
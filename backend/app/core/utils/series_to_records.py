import pandas as pd

def series_to_record(series: pd.Series, time_format = "iso") -> list:
    
    return [
        {"time": t, v: v}
        for t, v in zip(series.index, series.values)
    ]
import json
from pathlib import Path

def load_ticker_map() -> dict[str, str]:
    path = Path("app/json/stock_data.json")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
import io
import pytest
import pandas as pd
from app.services.portfolio_import_service import parse_csv
from app.models.positio import Position
from app import models
from sqlalchemy.exc import IntegrityError

def test_portfolio_import(test_db, test_portfolio, test_stock):

    csv_data = """Tulostuspäivä\tSalkku\tHankintapäivä\tInstrumentti\tTunnus\tISIN\tValuutta\tMäärä\tHankinta-arvo (Noteerausvaluutta)\tHankintahinta (EUR)
    7.10.2025\t19568203\t3.4.2024\tFortum\tFORTUM\tFI0009007132\tEUR\t10\t12.5\t125,0
    """

    fake_file = io.StringIO(csv_data)

    parse_csv(fake_file, portfolio_id=test_portfolio.id, db=test_db)

    positions = test_db.query(Position).all()
    assert len(positions) == 1
    assert positions[0].quantity == 10
    assert positions[0].buy_price == 12.5
    assert len(positions) != 2






    
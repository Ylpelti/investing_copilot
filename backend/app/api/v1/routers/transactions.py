from fastapi import APIRouter, Depends
from app.schemas.transactions import TransactionRead, TransactionCreate
from app.services.transaction.dependency import get_transaction_service
from app.services.transaction.transaction_service import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.post("/", response_model=TransactionRead)
def create_tx(
    transaction: TransactionCreate,
    tx_service: TransactionService = Depends(get_transaction_service)):
    return tx_service.create_transaction(transaction)



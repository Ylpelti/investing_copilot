from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.schemas.transactions import TransactionRead, TransactionCreate
from sqlalchemy.orm import Session
from app.crud.transaction_crud import TransactionCrud
from app.security.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.post("/", response_model=TransactionRead)
def create_tx(transaction: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tx_crud = TransactionCrud(db)
    return tx_crud.ceate_transaction(transaction, current_user.id)


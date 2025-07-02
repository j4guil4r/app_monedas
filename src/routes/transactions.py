from fastapi import APIRouter, HTTPException
from ..services.transaction_service import TransactionService
from decimal import Decimal

router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"]
)

@router.post("/transfer")
async def transfer_funds(
    sender_id: int,
    receiver_id: int,
    amount: float,
    api: str = "ExchangeRateAPI"
):
    try:
        amount_decimal = Decimal(str(amount))
        service = TransactionService()
        result = service.transfer(sender_id, receiver_id, amount_decimal, api)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/user/{user_id}")
async def get_user_transactions(user_id: int):
    try:
        service = TransactionService()
        transactions = service.get_user_transactions(user_id)
        
        return [{
            "id": t.id,
            "amount": float(t.amount),
            "currency": t.currency,
            "receiver_account_id": t.receiver_account_id,
            "exchange_rate": float(t.exchange_rate) if t.exchange_rate else None,
            "timestamp": t.timestamp.isoformat()
        } for t in transactions]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/deposit")
async def deposit_to_account(account_id: int, amount: float):
    try:
        service = TransactionService()
        result = service.deposit(account_id, Decimal(str(amount)))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
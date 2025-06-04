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
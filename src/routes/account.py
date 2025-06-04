from fastapi import APIRouter, HTTPException
from ..services.account_service import AccountService

router = APIRouter(prefix="/api/accounts", tags=["accounts"])
service = AccountService()

@router.post("/")
async def create_account(user_id: int, currency: str, balance: float = 0.0):
    try:
        account = service.create_account(user_id, currency, balance)
        return account
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/user/{user_id}")
async def get_user_accounts(user_id: int):
    try:
        accounts = service.get_user_accounts(user_id)
        return [{
            "id": acc.id,
            "currency": acc.currency,
            "balance": float(acc.balance)
        } for acc in accounts]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
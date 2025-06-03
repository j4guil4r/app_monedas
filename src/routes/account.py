from fastapi import APIRouter, HTTPException
from ..services.account_service import AccountService

router = APIRouter(prefix="/api/accounts", tags=["accounts"])

@router.post("/")
async def create_account(user_id: int, currency: str, balance: float = 0.0):
    try:
        service = AccountService()
        account = service.create_account(user_id, currency, balance)
        return account
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
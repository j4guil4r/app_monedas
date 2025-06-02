from fastapi import APIRouter, HTTPException
from ..services.exchange_service import ExchangeService

router = APIRouter(
    prefix="/api/exchange",
    tags=["exchange"]
)

@router.get("/convert")
async def convert_currency(
    amount: float,
    from_curr: str,
    to_curr: str
):
    try:
        service = ExchangeService()
        result = service.convert_currency(amount, from_curr, to_curr)
        return {
            "from_currency": from_curr,
            "to_currency": to_curr,
            "amount": amount,
            "converted_amount": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
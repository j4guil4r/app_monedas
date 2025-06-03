from fastapi import APIRouter, HTTPException
from ..services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/")
async def create_user(name: str):
    try:
        service = UserService()
        user = service.create_user(name)
        return {"id": user.id, "name": user.name}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
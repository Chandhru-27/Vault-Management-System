from fastapi import APIRouter

from app.api.v1.endpoints import auth, vaults, lockers, transactions

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(vaults.router, prefix="/vaults", tags=["vaults"])
api_router.include_router(lockers.router, prefix="/lockers", tags=["lockers"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

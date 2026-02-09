from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.future import select

from app.api.deps import AsyncSessionDep
from app.models.vault import Vault
from app.schemas.vault import VaultCreate, Vault as VaultSchema
from app.api.v1.endpoints.auth import get_current_admin_user, get_current_staff_user

router = APIRouter()

@router.post("/create", response_model=VaultSchema, status_code=status.HTTP_201_CREATED)
async def create_vault(
    vault_in: VaultCreate,
    db: AsyncSessionDep,
    current_admin: VaultSchema = Depends(get_current_admin_user)
):
    """
    Create a new vault (Admin only).
    """
    db_vault = Vault(
        location=vault_in.location,
        total_lockers=vault_in.total_lockers,
        available_lockers=vault_in.total_lockers,
        status=vault_in.status
    )
    db.add(db_vault)
    await db.commit()
    await db.refresh(db_vault)
    return db_vault

@router.get("/list", response_model=List[VaultSchema])
async def list_vaults(
    db: AsyncSessionDep,
    skip: int = 0,
    limit: int = 100,
    current_user: VaultSchema = Depends(get_current_staff_user)
):
    """
    Retrieve a list of vaults (Staff and Admin only).
    """
    result = await db.execute(select(Vault).offset(skip).limit(limit))
    vaults = result.scalars().all()
    return vaults

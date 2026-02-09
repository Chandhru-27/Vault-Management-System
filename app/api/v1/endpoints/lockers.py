from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import func

from app.api.deps import AsyncSessionDep
from app.models.vault import Vault
from app.models.locker import Locker
from app.models.locker_allocation import LockerAllocation
from app.models.user import User
from app.schemas.locker import LockerCreate, Locker as LockerSchema
from app.schemas.locker_allocation import LockerAllocationCreate, LockerAllocation as LockerAllocationSchema
from app.api.v1.endpoints.auth import get_current_active_user, get_current_staff_user

router = APIRouter()

async def _get_locker_and_vault_status(db: AsyncSessionDep, locker_id: int):
    """
    Helper function to fetch the locker and vault status
    """
    locker_result = db.execute(select(Locker).where(Locker.id == locker_id))
    locker = locker_result.scalars().first()

    vault_result = db.execute(select(Vault).where(Vault.id == locker.vault_id))
    vault = vault_result.scalars().first()
    return locker, vault

@router.post("/vaults/{vault_id}/", response_model=LockerSchema, status_code=status.HTTP_201_CREATED)
async def create_locker(
    vault_id: int,
    locker_in: LockerCreate,
    db: AsyncSessionDep,
    current_staff: User = Depends(get_current_staff_user)
):
    """
    Create a new locker within a vault (Staff and Admin only).
    """
    result = await db.execute(select(Vault).where(Vault.id == vault_id))
    vault = result.scalars().first()
    if not vault:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vault not found"
        )
    
    db_locker = Locker(
        vault_id=vault_id,
        locker_number=locker_in.locker_number,
        size=locker_in.size,
        status="AVAILABLE",
        monthly_rent=locker_in.monthly_rent
    )
    db.add(db_locker)
    vault.total_lockers += 1 
    vault.available_lockers += 1 
    await db.commit()
    await db.refresh(db_locker)
    await db.refresh(vault)
    return db_locker

@router.post("/{locker_id}/allocate", response_model=LockerAllocationSchema, status_code=status.HTTP_201_CREATED)
async def allocate_locker(
    locker_id: int,
    db: AsyncSessionDep,
    expiry_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Allocate a locker to a user (Active users).
    If no expiry_date is provided, defaults to 30 days from now.
    """
    locker, vault = await _get_locker_and_vault_status(db, locker_id)
    
    if vault and vault.status != "OPERATIONAL":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot allocate locker: vault is not operational"
        )
    
    if not locker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Locker not found")

    if locker.status != "AVAILABLE":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Locker is not available for allocation")

    if not vault or vault.available_lockers <= 0:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No available lockers in the vault")

    if expiry_date is None:
        expiry_date = datetime.utcnow() + timedelta(days=30)

    new_allocation = LockerAllocation(
        locker_id=locker_id,
        user_id=current_user.id,
        allocated_at=datetime.utcnow(),
        expiry_date=expiry_date,
        status="ACTIVE"
    )
    db.add(new_allocation)
    locker.status = "ALLOCATED"
    vault.available_lockers -= 1 

    await db.commit()
    await db.refresh(new_allocation)
    await db.refresh(locker)
    await db.refresh(vault)
    return new_allocation

@router.get("/available", response_model=List[LockerSchema])
async def check_available_lockers(
    db: AsyncSessionDep,
    size: str = None,
    vault_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Check for available lockers (Active users).
    """
    query = select(Locker).where(Locker.status == "AVAILABLE")
    if size:
        query = query.where(Locker.size == size.upper())
    if vault_id:
        query = query.where(Locker.vault_id == vault_id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    available_lockers = result.scalars().all()
    return available_lockers

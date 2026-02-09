from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.api.deps import AsyncSessionDep
from app.models.asset import Asset
from app.models.locker_allocation import LockerAllocation
from app.models.vault_transaction import VaultTransaction
from app.models.payment import Payment
from app.models.user import User
from app.schemas.asset import AssetCreate, Asset as AssetSchema
from app.schemas.transaction import VaultTransaction as VaultTransactionSchema
from app.schemas.payment import PaymentCreate, Payment as PaymentSchema
from app.api.v1.endpoints.auth import get_current_active_user

router = APIRouter()

@router.post("/allocations/{allocation_id}/assets", response_model=AssetSchema, status_code=status.HTTP_201_CREATED)
async def add_asset_to_locker(
    allocation_id: int,
    asset_in: AssetCreate,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_active_user)
):
    """
    Add an asset to an allocated locker (Active users).
    """
    result = await db.execute(
        select(LockerAllocation)
        .options(selectinload(LockerAllocation.user))
        .where(LockerAllocation.id == allocation_id)
    )
    allocation = result.scalars().first()

    if not allocation or allocation.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Locker allocation not found for current user")
    
    if allocation.status == "EXPIRED":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot add asset to an expired allocation")

    db_asset = Asset(
        allocation_id=allocation_id,
        asset_name=asset_in.asset_name,
        estimated_value=asset_in.estimated_value,
        type=asset_in.type
    )
    db.add(db_asset)
    db_transaction = VaultTransaction(
        allocation_id=allocation_id,
        type="DEPOSIT"
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_asset)
    await db.refresh(db_transaction)
    return db_asset

@router.delete("/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_asset_from_locker(
    asset_id: int,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove an asset from an allocated locker (Active users).
    """
    result = await db.execute(
        select(Asset)
        .options(selectinload(Asset.allocation).selectinload(LockerAllocation.user))
        .where(Asset.id == asset_id)
    )
    db_asset = result.scalars().first()

    if not db_asset or db_asset.allocation.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found for current user")

    db_transaction = VaultTransaction(
        allocation_id=db_asset.allocation_id,
        type="WITHDRAW"
    )
    db.add(db_transaction)
    await db.delete(db_asset)
    await db.commit()
    return

@router.post("/allocations/{allocation_id}/pay_rent", response_model=PaymentSchema, status_code=status.HTTP_201_CREATED)
async def pay_rent_for_locker(
    allocation_id: int,
    payment_in: PaymentCreate,
    db: AsyncSessionDep,
    current_user: User = Depends(get_current_active_user)
):
    """
    Process rent payment for a locker allocation (Active users).
    Extends expiry date by one month upon successful payment.
    """
    result = await db.execute(
        select(LockerAllocation)
        .options(selectinload(LockerAllocation.user))
        .where(LockerAllocation.id == allocation_id)
    )
    allocation = result.scalars().first()

    if not allocation or allocation.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Locker allocation not found for current user")
    
    db_payment = Payment(
    allocation_id=allocation_id,
    amount=payment_in.amount,
    status="SUCCESSFUL"
    )
    db.add(db_payment)

    allocation.expiry_date += timedelta(days=30)
    allocation.status = "ACTIVE"

    await db.commit()
    await db.refresh(db_payment)
    await db.refresh(allocation)
    return db_payment

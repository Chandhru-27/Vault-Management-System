from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal

async def get_db() -> Generator[AsyncSession, None, None]:
    async with SessionLocal() as session:
        yield session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]

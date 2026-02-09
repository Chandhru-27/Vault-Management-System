from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.base import Base
from app.db.session import engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Vault Management System API",
    openapi_url="/api/v1/openapi.json"
)

# Include API routers
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Vault Management System API"}


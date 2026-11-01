from database import create_table
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.reviews import router as reviews_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    print("the table is created")
    yield
    print("the table shut down")
app = FastAPI(
    title="Review API",
    description="rangmanch api Review API",
    lifespan=lifespan,
)
app.include_router(reviews_router)
@app.get("/")
async def root():
    return {"message": "welcome to rangmanch API"}
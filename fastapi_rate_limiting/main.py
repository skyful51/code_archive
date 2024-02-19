import redis.asyncio as redis
import uvicorn
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, APIRouter

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()

app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix="/limit")

@router.get("/get", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def index():
    return {"msg": "Hello World"}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
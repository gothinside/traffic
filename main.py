from fastapi import FastAPI
from db import engine, SessionLocal
from models import Base
import asyncio
from grpc_core.server import Server
from contextlib import asynccontextmanager
import logging
from api import traffic

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Запускает gRPC сервер и инициализирует базу данных при старте.
    """
    server = Server(SessionLocal)
    asyncio.create_task(server.serve())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await server.stop()
        await engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(router=traffic.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

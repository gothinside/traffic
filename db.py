from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import DB_URL


engine = create_async_engine(f"sqlite+aio{DB_URL}", future=True, echo=True)


Base = declarative_base()
Base.metadata.bind = engine

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=True,
    class_=AsyncSession)



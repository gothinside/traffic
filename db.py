from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_async_engine("sqlite+aiosqlite:///traffic_db.db", future=True, echo=True)


Base = declarative_base()
Base.metadata.bind = engine

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=True,
    class_=AsyncSession)



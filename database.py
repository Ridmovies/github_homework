from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

# URL = "sqlite+aiosqlite:///:memory:"
URL = "sqlite+aiosqlite:///database.db"

async_engine = create_async_engine(URL, echo=True)
async_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)
session = async_session()

Base = declarative_base()

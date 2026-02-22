from typing import Any

from sqlalchemy import Boolean, Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), unique=True, nullable=False)
    active = Column(Boolean, nullable=False, default=True)


engine = create_async_engine(settings.async_db_url, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


def serialize_user(user: User) -> dict[str, Any]:
    return {"id": user.id, "email": user.email, "active": user.active}


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_users() -> list[dict[str, Any]]:
    async with SessionLocal() as session:
        result = await session.execute(select(User).order_by(User.id))
        return [serialize_user(user) for user in result.scalars().all()]


async def get_or_create_user(email: str) -> dict[str, Any]:
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user is None:
            user = User(email=email, active=True)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return serialize_user(user)


async def dispose_engine() -> None:
    await engine.dispose()

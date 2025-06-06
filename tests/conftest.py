import json

from src.config import settings
from src.main import app
from src.models import *
from src.database import Base, engine_null_pool, async_session_maker_with_null_pull
from httpx import ASGITransport, AsyncClient
from src.schemas.hotels import HotelAdd

import pytest

from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", 'r') as f_hotels:
        hotels_data = json.load(f_hotels)

    with open("tests/mock_rooms.json", 'r') as f_rooms:
        rooms_data = json.load(f_rooms)

    async with DBManager(session_factory=async_session_maker_with_null_pull) as db:
        await db.hotels.add_bulk([HotelAdd(**hotel) for hotel in hotels_data])
        await db.rooms.add_bulk([RoomAdd(**room) for room in rooms_data])
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def test_register_user(setup_database):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.ru",
                "password": "12345"
            }
        )

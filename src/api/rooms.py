from fastapi import Query, APIRouter, Body

from src.repos.rooms import RoomsRepository
from src.schemas.rooms import RoomPATCH, RoomAdd
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        title: str | None = Query(None, description="Название номера"),
        price: int | None = Query(None, description="Цена номера"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            price=price,
        )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("{hotel_id}/rooms")
async def create_room(
        room_data: RoomAdd = Body(openapi_examples={
            "1": {
                "summary": "Создание номера",
                "value": {
                    "title": "1-местный номер стандарт",
                    "hotel_id": 1,
                    "price": 6400,
                    "quantity": 10,
                    "description": (
                            "В номере: кровать полутораспальная (120*190 см), сейф, прикроватная тумба, "
                            "кресло, шкаф, письменный стол, стул, телевизор (спутниковое телевидение), "
                            "зеркало, телефон, торшер. Санузел: 3.0 м²: душевая кабина, зеркало, "
                            "полотенца, гигиенический набор (мыло, шампунь, гель для душа)."
                    )
                }
            }
        }),
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("{hotel_id}/room/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAdd
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).edit(
            hotel_id=hotel_id,
            id=room_id,
            data=room_data
        )
        await session.commit()
    return {"status": "OK", "data": room}


@router.patch("{hotel_id}/room/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPATCH
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).edit(
            room_data,
            exclude_unset=True,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    return {"status": "OK", "data": room}


@router.delete("{hotel_id}/room/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}

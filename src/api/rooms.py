from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomPatch, RoomPatchRequest, RoomAdd, RoomAddRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("{hotel_id}/rooms")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {
                "summary": "Создание номера",
                "value": {
                    "title": "1-местный номер стандарт",
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.add(_room_data)

    room_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(room_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("{hotel_id}/room/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    room = await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.update_room_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()

    return {"status": "OK", "data": room}


@router.patch("{hotel_id}/room/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))

    room = await db.rooms.edit(
        _room_data,
        hotel_id=hotel_id,
        id=room_id,
        exclude_unset=True
    )
    await db.rooms_facilities.update_room_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()

    return {"status": "OK", "data": room}


@router.delete("{hotel_id}/room/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.close()
    return {"status": "OK"}

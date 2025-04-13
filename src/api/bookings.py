from fastapi import APIRouter

from src.api.dependencies import UserIdDep
from src.api.dependencies import DBDep
from src.schemas.bookings import AddBookingRequest, AddBooking

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(
        booking_data: AddBookingRequest,
        db: DBDep,
        user_id: UserIdDep,
):
    room_price = (await db.rooms.get_one_or_none(id=booking_data.room_id)).price
    _booking_data = AddBooking(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_user_bookings(user_id: UserIdDep, db: DBDep, ):
    return await db.bookings.get_filtered(user_id=user_id)

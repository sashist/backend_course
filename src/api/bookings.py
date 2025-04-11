from fastapi import APIRouter
from datetime import date

from src.api.dependencies import get_current_user_id, get_token, UserIdDep
from src.api.dependencies import DBDep
from src.schemas.bookings import AddBookingRequest, AddBooking

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(
        booking_data: AddBookingRequest,
        db: DBDep,
        user_id: UserIdDep,
):

    price = (await db.rooms.get_one_or_none(id=booking_data.room_id)).price
    _booking_data = AddBooking(
        user_id=user_id,
        price=price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}

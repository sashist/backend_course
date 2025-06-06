from datetime import date

from asyncpg.pgproto.pgproto import timedelta

from src.schemas.bookings import BookingAdd, Booking


async def test_add_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.users.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(2025, 8, 10),
        date_to=date(2025, 8, 20),
        price=500.0
    )
    #CREATE
    new_booking = await db.bookings.add(booking_data)

    #READ
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking is not None

    #UPDATE
    booking_data.date_to += timedelta(days=2)
    await db.bookings.edit(data=booking_data, exclude_unset=True, id=booking.id)
    edit_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert edit_booking.date_to == date(2025, 8, 22)
    
    #DELETE
    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking is None

    await db.commit()

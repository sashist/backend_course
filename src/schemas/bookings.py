from pydantic import BaseModel, ConfigDict
from datetime import date


class AddBooking(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class AddBookingRequest(BaseModel):
    room_id: int
    date_to: date
    date_from: date


class Booking(AddBooking):
    id: int

    model_config = ConfigDict(from_attributes=True)

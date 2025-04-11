from src.repos.base import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking  # Define the schema if needed


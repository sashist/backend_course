from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repos.base import BaseRepository
from src.models.rooms import RoomsORM
from src.repos.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )

        res = await self.session.execute(query)
        model = res.scalars().one_or_none()

        return RoomWithRels.model_validate(model) if res else None

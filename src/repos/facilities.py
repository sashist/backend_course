from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repos.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityAdd
from src.schemas.rooms import Room


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

    async def update_room_facilities(
            self,
            room_id: int,
            facilities_ids: list[int],
    ):
        room_facilities = [room.facility_id for room in (await self.get_filtered(room_id=room_id))]
        facilities_to_add = [f_id for f_id in facilities_ids if f_id not in room_facilities]
        facilities_to_remove = [f_id for f_id in room_facilities if f_id not in facilities_ids]

        if facilities_to_add:
            room_facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in facilities_to_add]
            await self.add_bulk(room_facilities_data)

        if facilities_to_remove:
            for f_id in facilities_to_remove:
                await self.delete(room_id=room_id, facility_id=f_id)

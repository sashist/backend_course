from fastapi import Query, APIRouter, Body


from repos.hotels import HotelsRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependecies import PaginationDep
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес"),

):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all()
    # per_page = pagination.per_page or 5
    #     query = selec t(HotelsORM)
    #     if title:
    #         query = (
    #             query
    #             .filter(HotelsORM.title.ilike(f'%{title.strip()}%'))
    #         )
    #     if location:
    #         query = (
    #             query
    #             .filter(HotelsORM.location.ilike(f'%{location.strip()}%'))
    #         )
    #     query = (
    #         query
    #         .limit(per_page)
    #         .offset(per_page * (pagination.page - 1))
    #     )
    #     result = await session.execute(query)
    #
    #     hotels = result.scalars().all()
    #
    #     return hotels

    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    # return hotels_

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)
@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "sochi_u_morya",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "location": "dubai_fountain",
        }
    }
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}



@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await  session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await  session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}

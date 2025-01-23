from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()


@app.get("/")
def func():
    return "Hello world!!"


hotels = [
    {"id": 1, "title": "Sochi", "name": "Omega"},
    {"id": 2, "title": "Dubai", "name": "Aqua"}
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Номер"),
        title: str | None = Query(None, description="Название отеля")
):
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]


@app.delete("/hotels/{hotels_id}")
def delete_hotel(hotels_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotels_id != hotel['id']]
    return {'status': 'ok'}


@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True, description="Название города")
        title: str = Body(embed=True, description="Название отеля")
):
    hotels.append(
        {'id': hotels[-1]['id'] + 1,
         'title': title}
    )
    return {"status": "ok"}


@app.put("/hotels/{hotel_id}")
def full_edit_hotel(
        id: int,
        title: str = Body(description="Заголовок"),
        name: str = Body(description="Название")
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == id:
            hotel["title"] = title
            hotel["name"] = name
    return {'status': 'ok'}


@app.patch("/hotels/{hotel_id}")
def edit_hotel(
        id: int,
        title: str | None = Body(description="Заголовок"),
        name: str | None = Body(description="Название")

):
    global hotels
    for hotel in hotels:
        if hotel["id"] == id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
    return {'status': 'ok'}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

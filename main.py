from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()


@app.get("/")
def func():
    return "Hello world!!"


hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Dubai"}
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Номер"),
        title: str | None = Query(None, description="Название отеля")
):
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

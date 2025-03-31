from pydantic import BaseModel, Field


class RoomAdd(BaseModel):
    title: str
    hotel_id: int
    price: int
    quantity: int
    description: str | None = Field(None)


class Room(RoomAdd):
    id: int

    # model_config = ConfigDict(from_attributes=True)


class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    description: str | None = Field(None)

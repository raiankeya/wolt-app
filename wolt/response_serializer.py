from pydantic import BaseModel, Field


class Event(BaseModel):
    type: str
    value: int


class WeekdaysEvent(BaseModel):
    monday: list[Event] | None = Field(nullable=True)
    tuesday: list[Event] | None = Field(nullable=True)
    wednesday: list[Event] | None = Field(nullable=True)
    thursday: list[Event] | None = Field(nullable=True)
    friday: list[Event] | None = Field(nullable=True)
    saturday: list[Event] | None = Field(nullable=True)
    sunday: list[Event] | None = Field(nullable=True)

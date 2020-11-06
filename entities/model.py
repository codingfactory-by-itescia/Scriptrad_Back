from datetime import date ,datetime
from pydantic import BaseModel
from bson import ObjectId

class Transcript(BaseModel):
    file: str

class Traduce(BaseModel):
    text: str

class Summarize(BaseModel):
    text: str

class Reservation(BaseModel):
    _id: ObjectId
    TaskID: int
    OwnerID: int
    Title: str
    Description: str
    StartTimezone: datetime
    Start: datetime
    End: datetime
    EndTimezone: datetime
    RecurrenceRule: int
    RecurrenceID: int
    RecurrenceException: int
    IsAllDay: bool

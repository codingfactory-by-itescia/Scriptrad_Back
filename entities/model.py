from datetime import date ,datetime
from pydantic import BaseModel

class Transcript(BaseModel):
    file: str

class Traduce(BaseModel):
    text: str

class Summarize(BaseModel):
    summary: str
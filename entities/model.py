from datetime import date ,datetime
from pydantic import BaseModel

class Translate(BaseModel):
    file: str

class Traduce(BaseModel):
    text: str

class Resume(BaseModel):
    traduction: str
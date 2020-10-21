from typing import Optional
from entities.model import *
from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Scriptrad",
    description="Translation/traduction API",
    version="1.0"
)

@app.post("/translate")
def translate(translate: Translate):
    return "la"

@app.post("/traduce")
def traduce(traduce: Traduce):
    print("la")

@app.post("/resume")
def resume(resume: Resume):
    print("la")
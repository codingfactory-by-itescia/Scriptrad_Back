from typing import Optional
from entities.model import *
from fastapi import FastAPI
from datetime import datetime
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech

app = FastAPI(
    title="Scriptrad",
    description="Translation/traduction API",
    version="1.0"
)

@app.post("/translate")
def translate(translate: Translate):

    # Json file about API Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), "resources", "api_key.json")

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(os.path.dirname(__file__), "resources", "Enregistrement.mp3")

    # Loads the audio into memory
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

@app.post("/traduce")
def traduce(traduce: Traduce):
    print("la")

@app.post("/resume")
def resume(resume: Resume):
    print("la")
from typing import Optional
from entities.model import *
from fastapi import FastAPI
from datetime import datetime
import subprocess, sys, io, pathlib, os
# Accept link between Python and Angular (Rest)
from fastapi.middleware.cors import CORSMiddleware
# Imports the Google Cloud client library
from google.cloud import speech


app = FastAPI(
    title="Scriptrad",
    description="Translation/traduction API",
    version="1.0"
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
	"http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/sendAudioByGet/{file_name}")
def read_item(file_name: str):
    return file_name
#end tests

# @app.post("/transcript")
# def translate(transcript: Transcript):
#     return transcript.file
@app.post("/transcript")
def transcript(transcript: Transcript):

    # Json file about API Key and credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), "resources", "api_key.json")

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    absolute_current_path = pathlib.Path().absolute()
    folder_name = "resources"
    filename = "Enregistrement.mp3"
    absolute_path = os.path.join(absolute_current_path, folder_name, filename)
    print("CHEMIN --> ", absolute_path)
    sys.exit()
    absolute_folder_path = os.path.join(absolute_current_path, folder_name)
    subprocess.check_output(['sox',absolute_folder_path,'--channels=1','--bits=16',filename]) 

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

@app.post("/summarize")
def resume(summarize: Summarize):
    print("la")
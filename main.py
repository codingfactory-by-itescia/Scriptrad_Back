from typing import Optional
from entities.model import *
from fastapi import FastAPI
from datetime import datetime
import subprocess, sys, json, io, pathlib, os, proto
from google.protobuf.json_format import MessageToJson

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

    base = os.path.splitext(translate.file)[0]

    folder_name = "uploads"
    filename = translate.file
    flac_filename = base+".flac"

    absolute_path = os.path.join(absolute_current_path, folder_name, filename)
    absolute_folder_path = os.path.join(absolute_current_path, folder_name)
    absolute_folder_flac = os.path.join(absolute_folder_path,flac_filename)
    subprocess.check_output(['sox', absolute_path, absolute_folder_flac]) 

    # Loads the audio into memory
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        audio_channel_count=2,
        language_code="fr-FR",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

    #print(response.results[0])
    #sys.exit()
    json_string = proto.Message.to_json(response.results[0])
    response = json_string.replace('\n', '') 
    return response

@app.post("/traduce")
def traduce(traduce: Traduce):
    print("la")

@app.post("/summarize")
def resume(summarize: Summarize):
    print("la")
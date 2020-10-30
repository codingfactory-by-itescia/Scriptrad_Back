from typing import Optional
from entities.model import *
from fastapi import FastAPI
from datetime import datetime
import subprocess, sys, json, io, pathlib, os, proto
from google.protobuf.json_format import MessageToJson
from fastapi.middleware.cors import CORSMiddleware
# from summarize import Summarizer

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

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

    base = os.path.splitext(transcript.file)[0]

    folder_name = "uploads"
    filename = transcript.file
    flac_filename = base+".flac"

    absolute_path = os.path.join(absolute_current_path, folder_name, filename)
    absolute_folder_path = os.path.join(absolute_current_path, folder_name)
    absolute_folder_flac = os.path.join(absolute_folder_path,flac_filename)
    subprocess.check_output(['sox', absolute_path, absolute_folder_flac]) 

    # Loads the audio into memory
    with io.open(absolute_folder_flac, "rb") as audio_file:
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

#summarize

def read_article( file_name):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []

    for sentence in article:
        print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()

    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

#top_n number of paragraphs without blank line
def generate_summary(file_name, top_n=3):
    stop_words = stopwords.words('french')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_article(file_name)
    return sentences
    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    print("Indexes of top ranked_sentence order are ", ranked_sentence)

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Step 5 - Offcourse, output the summarize texr
    print("Summarize Text: \n", ". ".join(summarize_text))

    #Step 6 return
    return ("Summarize Text: \n", ". ".join(summarize_text))

@app.post("/summarize")
def resume(summarize: Summarize):
    #s = Summarizer()
    print("la")
    return generate_summary("testSummarize - Copie.txt")
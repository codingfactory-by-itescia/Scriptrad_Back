import pyaudio, wave
from datetime import datetime
import sys

d = datetime.now()

# recording configs
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = d.strftime('%Y-%m-%d-%H-%M-%S')+".wav"

# create & configure microphone
mic = pyaudio.PyAudio()
stream = mic.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

stream.start_stream()
print("=== ENREGISTREMENT EN COURS ====")

#Recording data until under threshold
frames=[]

while True:
    #Converting chunk data into integers
    data = stream.read(CHUNK, exception_on_overflow = False)
    #Recording chunk data
    frames.append(data)
    if sys.argv[1] == "stop":
        break

# read & store microphone data per frame read
'''frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK, exception_on_overflow = False)
    frames.append(data) '''

print("==== ENREGISTREMENT EFFECTUE ====")

# kill the mic and recording
stream.stop_stream()
stream.close()
#mic.terminate()

# combine & store all microphone data to output.wav file
outputFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
outputFile.setnchannels(CHANNELS)
outputFile.setsampwidth(mic.get_sample_size(FORMAT))
outputFile.setframerate(RATE)
outputFile.writeframes(b''.join(frames))
outputFile.close()
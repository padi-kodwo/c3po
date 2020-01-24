import logging as logger
import logging.config
import os
import sys
import time
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
# from request import Dialogflow
from flask_cors import CORS
from flask import render_template
import requests
import wave
from flask import Flask
from flask import request
from deepspeech import Model
from scipy.io import wavfile
import os.path

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def process_file():
    print("hit the point")
    wav = request.files['audio']
    print(request)
    filepath = os.getcwd() +"/" + wav.filename
    wav.save(filepath)
    fs, audio = wavfile.read(filepath)
    r = sr.Recognizer()
    # start_time = time.time()
    hellow = sr.AudioFile(filepath)
    logger.info("calling google to recognise speech")
    with hellow as source:
        audio = r.record(source)
    try:
        s = r.recognize_google(audio)
        print("Text: " + s)
    except Exception as e:
        print("Exception: " + str(e))
        # print("--- %s seconds ---" % (time.time() - start_time))
    return r.recognize_google(audio)


# def get_speech_from_text(text, language, file_name):
#     if text is not None and language is not None and file_name is not None:
#
#         speech_from_text = gTTS(text=text, lang=language, slow=False)
#         speech_from_text.save(file_name)
#         return file_name
#     else:
#         logger.warning("please pass all params")
#         return
@app.route('/page')
def page():
    return render_template('voice_ai.html')



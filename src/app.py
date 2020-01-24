import logging as logger
import logging.config
import os
import sys
import time
from io import BytesIO

import speech_recognition as sr
from gtts import gTTS
import pyttsx3
from src.request import Dialogflow

import sounddevice as sd
from playsound import playsound
import pygame
from scipy.io.wavfile import write


# application configs goes here
logger.config.fileConfig(os.path.dirname(__file__) + "/resource/config/logger.conf")

# Globals
engine = pyttsx3.init()
engine.setProperty('rate', 125)


# test to speech synthesiser
def prompt_c3po(text):
    start = time.time()
    if not isinstance(text, str):
        raise TypeError("must be a string")

    print("[c3po] " + text)
    engine.say(text)
    engine.runAndWait()
    # logger.info("time elapsed: " + str(time.time() - start))
    return


# Google's text to speech API implementation
def prompt_c3po_gtts(text):
    start = time.time()

    if not isinstance(text, str):
        raise TypeError("must be a string")

    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    print("here")
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    print("[c3po] " + text)
    logger.info("time elapse: ", time.time() - start)

    # logger.info("time elapsed: " + str(time.time() - start))
    return


def main():
    start_time = time.time()
    choice = 1
    audio_path = "jackhammer.wav"

    if choice == 1:
        # say greetings
        intro_message = "Hi! I'm c3PO, your rendezvous voice AI "
        prompt_c3po(intro_message)

        # live microphone stream
        # create recognizer and mic instances
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        count = 0

        while True:
            if count < 1:
                prompt_c3po("how can i help you?")

            transcription_response = recognise_stream(recognizer, microphone)

            if transcription_response["transcription"]:
                print("[you]: " + transcription_response["transcription"])
                if transcription_response["transcription"]:
                    time.sleep(1)
                    print("[c3po]: thinking")
                    dialog_flow_obj = Dialogflow(transcription_response["transcription"])
                    dialog_flow_respond = dialog_flow_obj.get_kb_response()
                    prompt_c3po(dialog_flow_respond.query_result.fulfillment_text)
                    goodbye(transcription_response["transcription"])
            else:
                if transcription_response["success"]:
                    prompt_c3po("I can't hear you, please come again")
                else:
                    prompt_c3po("I'm having some trouble connecting to the internet")

            count += 1

    else:
        # recorded sample is live
        transcription_response = recognise_recording(audio_path)
        print(transcription_response)
        return


# Transcribe speech from recorded from `microphone`
def recognise_stream(recogniser, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recogniser, sr.Recognizer):
        raise TypeError("must be a recogniser instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("must be a microphone instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        start_time = time.time()
        recogniser.adjust_for_ambient_noise(source)
        logger.info("listening ...")
        audio = recogniser.listen(source)

        logger.info("calling google to recognise speech")
        # set up the response object
        response = {
            "success": None,
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = recogniser.recognize_google(audio)
            response["success"] = True
            print(response)
            logger.info("successful api call to google")

        except sr.RequestError as request_error:
            # API was unreachable or unresponsive
            logger.warning(request_error)
            response["success"] = False
        except sr.UnknownValueError as unknown_value_error:
            # speech was unintelligible
            logger.warning(unknown_value_error)
            response["success"] = True
            response["error"] = "Unable to recognize speech"

        end_time = time.time() - start_time
        print("time elapsed: ", end_time)

        return response


# takes the audio file path and return to console the text
def recognise_recording(audio_source_path):
    recognizer = sr.Recognizer()
    source_audio_path = os.path.dirname(__file__) + "/output/audio/" + audio_source_path
    copy_audio_path = os.path.dirname(__file__) + "/output/audio/1" + audio_source_path
    audio_file = sr.AudioFile(source_audio_path)

    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

        print(type(audio.get_wav_data()))

        print("waiting for google response(audio_file) ...")
        start_time = time.time()

        logger.info("calling google to recognise audio speech")
        # set up the response object
        response = {
            "success": None,
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = recognizer.recognize_google(audio)
            logger.info("successful api call to google")
            response["success"] = True

        except sr.RequestError:
            # API was unreachable or unresponsive
            logger.warning("Api was 404")
            response["success"] = False
        except sr.UnknownValueError:
            # speech was unintelligible
            logger.warning("speech was unintelligible")
            response["success"] = True
            response["error"] = "Unable to recognize speech"

        end_time = time.time() - start_time
        print("time elapsed: ", end_time)

        return response


# Play audio in audio path passed
def play_audio(audio_file_path):
    playsound(audio_file_path)


# Goodbye intent module
def goodbye(test_from_speech):
    if "goodbye" in test_from_speech.strip():
        prompt_c3po("ok, good bye")
        logger.info("exit triggered")
        sys.exit()
    else:
        return


def get_speech_from_text(text, language, file_name):
    if text is not None and language is not None and file_name is not None:
        speech_from_text = gTTS(text=text, lang=language, slow=False)
        speech_from_text.save(file_name)
        return file_name
    else:
        logger.warning("please pass all params")
        return


def record_audio_from_mic():
    fs = 44100  # Sample rate
    seconds = 4  # Duration of recording
    my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    audio_path = os.path.dirname(__file__) + "/output/audio/sample.wav"
    write(audio_path, fs, my_recording)  # Save as WAV file


def get_wav_from_audio_bytes(audio, copy_audio_path):
    with open(copy_audio_path, "wb") as f:
        f.write(audio.get_wav_data())

def c3po():
    pygame.init()
    main()

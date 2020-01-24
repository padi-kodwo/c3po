import logging as logger
import logging.config
import os
import system_paths
import time
from io import BytesIO

import speech_recognition as sr
from gtts import gTTS



# application configs goes here
from src.request import Dialogflow

logger.config.fileConfig(system_paths.resource + "/config/logger.conf")

# Globals
recognizer = sr.Recognizer()


def respond(wav_file_path):
    if os.path.isfile(wav_file_path):
        logger.info("request audio found")

        transcription_response = recognise_recording(wav_file_path)

        if transcription_response["transcription"]:
            print("[you]: " + transcription_response["transcription"])
            if transcription_response["transcription"]:
                dialog_flow_obj = Dialogflow(transcription_response["transcription"])
                dialog_flow_respond = dialog_flow_obj.get_kb_response()
                return text_to_speech(dialog_flow_respond.query_result.fulfillment_text)
        else:
            if transcription_response["success"]:
                return text_to_speech("I can't hear you, please come again")
            else:
                return text_to_speech("I'm having some trouble connecting to the internet")

    else:
        logger.warning(str(wav_file_path) + " not found in file system")
        return None


def recognise_recording(audio_source_path):
    audio_file = sr.AudioFile(audio_source_path)

    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

        logger.info("waiting for google response(audio_file) ...")
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


def text_to_speech(text):
    language = "en"
    text_audio = gTTS(text=text, lang=language, slow=False)

    return text_audio


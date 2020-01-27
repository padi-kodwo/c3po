import logging as logger
import logging.config
import os
import system_paths
import time

import speech_recognition as sr
from gtts import gTTS


# application configs goes here
from src.request import Dialogflow

# configure the logging format
logger.config.fileConfig(system_paths.resource + "/config/logger.conf")

# Globals
recognizer = sr.Recognizer()


def respond(wav_file_path):
    if os.path.isfile(wav_file_path):
        logger.info("request audio found in data store")

        transcription_response = recognise_recording(wav_file_path)

        if transcription_response["transcription"]:
            logger.info("response from speech recognition is " + str(transcription_response["transcription"]))

            if transcription_response["transcription"]:
                logger.info("about to call dialog flow speech response")
                dialog_flow_obj = Dialogflow(transcription_response["transcription"])
                dialog_flow_respond = dialog_flow_obj.get_kb_response()
                logger.info("about to get audio response")
                if dialog_flow_respond.query_result.fulfillment_text is None or dialog_flow_respond.query_result.fulfillment_text is "":
                    logger.info("response fulfilment was empty or None")
                    return text_to_speech("Haha")
                else:
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
        start_time = time.time()
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

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

        duration = time.time() - start_time
        logger.info("time elapsed: " +str(duration))

        logger.info("done with speech recognition ")

        return response


def text_to_speech(text):
    logger.info("about to synthesis text audio ")
    file_destination = os.path.join(system_paths.data_store, "response.wav")
    language = "en"

    text_audio = gTTS(text=text, lang=language, slow=False)
    logger.info("audio fp return from google")
    text_audio.save(os.path.join(system_paths.data_store, file_destination))
    logger.info("done synthesising text to audio")

    return file_destination





import logging as logger
import logging.config
import os
import sys
import time
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from request import Dialogflow

# application configs goes here
logger.config.fileConfig(os.path.dirname(__file__) + "/resources/config/logger.conf")


def prompt_c3po(text, file_name):
    message_file = os.path.dirname(__file__) + "/resources/audio/" + file_name

    if os.path.isfile(message_file):
        print("[c3po] " + text)
        play_audio(message_file)
    else:
        get_speech_from_text(text=text, language="en", file_name=message_file)
        print("[c3po] " + text)
        play_audio(message_file)
    return


def man():
    start_time = time.time()
    choice = 1
    harvard_audio_path = os.path.dirname(__file__) + "/resources/audio/harvard.wav"

    if choice == 1:
        # say greetings
        intro_message = "Hi! I'm c3PO, your rendezvous voice AI "
        prompt_c3po(intro_message, "intro.wav")

        # live microphone stream
        # create recognizer and mic instances
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        count = 0

        while True:
            prompt_c3po("say something, I'm listening", "say_something.wav")
            transcription_response = recognise_stream(recognizer, microphone)

            if transcription_response["transcription"]:
                print("[you]: " + transcription_response["transcription"])
                print("[c3po]: thinking")
                dialog_flow_obj = Dialogflow(transcription_response["transcription"])
                dialog_flow_respond = dialog_flow_obj.get_kb_response()
                prompt_c3po(dialog_flow_respond.query_result.fulfillment_text, str(count) + ".wav")
            count += 1
            if transcription_response["error"]:
                prompt_c3po("I'm having some trouble connecting to the internet", "error" + str(
                    count) + ".wav")
            else:
                prompt_c3po("I can't hear you, please come again", "please_come_again.wav")
    else:
        # recorded sample is live
        print("recorded sample is live")
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
        audio = recogniser.listen(source)

        logger.info("calling google to recognise speech")
        # set up the response object
        response = {
            "success": None,
            "error": None,
            "transcription": None
        }

        try:
            logger.info("successful api call to google")
            response["transcription"] = recogniser.recognize_google(audio)
            response["success"] = True

        except sr.RequestError:
            # API was unreachable or unresponsive
            logger.warning("Api was 404")
            response["success"] = False
        except sr.UnknownValueError:
            # speech was unintelligible
            logger.warning("speech was unintelligible")
            response["error"] = "Unable to recognize speech"
            response["success"] = True

        end_time = time.time() - start_time
        print("time elapsed: ", end_time)

        return response


# Play audio in audio path passed
def play_audio(audio_file_path):
    playsound(audio_file_path)


# Goodbye intent module
def goodbye(test_from_speech):
    if test_from_speech == "goodbye":
        print("c3po: ok, good bye")
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


if __name__ == '__main__':
    man()

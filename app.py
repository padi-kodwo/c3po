import logging as logger
import os
import sys
import time
import dialogflow

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Pools-Agent-12-ae9f87bbd9b2.json'
DIALOGFLOW_PROJECT_ID = 'pools-agent-12'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

class Dialogflow:
    def __init__(self,text):
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        print(self.session)
        pass
    def get_kb_response(self, query):
        text_input = dialogflow.types.TextInput(text=query, language_code=DIALOGFLOW_LANGUAGE_CODE)
        print(text_input)
        query = dialogflow.types.QueryInput(text=text_input)

        try:
            print(query)
            response = self.session_client.detect_intent(session=self.session, query_input=query)
            return response
        except InvalidArgument as e:
            print(f"something went wrong {e}")
            pass
        pass
    pass


        
def _call_():
    text = input("Enter your text")
    print(text)
    dialogflow = Dialogflow(text)
    response = dialogflow.get_kb_response(text)
    print(response)



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
        print("[c3po] " + intro_message)
        prompt_c3po(intro_message, "intro.wav")

        # live microphone stream
        # create recognizer and mic instances
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        count = 0

        while True:
            prompt_c3po("say something, I'm listening", "say_something.wave")
            response = recognise_stream(recognizer, microphone)

            if response["transcription"]:
                print("[you] " + response["transcription"])

                ## dialog flow goes here
                return
        count += 1
    else:
        # recorded sample is live
        print("recorded sample is live")


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

        logger.info("calling google speech api")

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            logger.info("successful api call to google")
            response["transcription"] = recogniser.recognize_google(audio)

        except sr.RequestError:
            # API was unreachable or unresponsive
            logger.warning("Api was 404")

            response["success"] = False
            response["transcription"] = "I'm having some trouble connecting to the internet"

        except sr.UnknownValueError:
            # speech was unintelligible
            logger.warning("speech was unintelligible")

            response["error"] = "Unable to recognize speech"
            response["transcription"] = "can you talk a little louder"

        end_time = time.time() - start_time
        print("time elapsed: ", end_time)

        return response


# Get intent and its resolution from dialog flow
def dialog_flow_respond(text):
    return text


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

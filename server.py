# serve.py
import logging as logger
import logging.config
import time
import os
import system_paths
from flask_cors import CORS
from waitress import serve
from flask import Flask, render_template, request, send_file, redirect, jsonify


# creates a Flask application, named app
app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)
# configure the logging format
logger.config.fileConfig(system_paths.resource + "/config/logger.conf")


# a route where we will display a welcome message via an HTML template
@app.route("/abc")
def index():
    message = "Welcome to the beautiful experience"
    return render_template('index.html', message=message)


@app.route("/")
def home():
    return render_template("voice_ai.html")


# the bot controller endpoint for all dialogue
@app.route("/c3p0", methods=["POST"])
def bot_controller():
    logger.info("about to process dialog audio")
    request_audio_wav = request.files['audio']
    logger.info("done getting audio from request")

    # saving audio request to data store for processing
    import src.util.util as util
    wav_file = util.save_audio_request(request_audio_wav)
    logger.info("audio saved successfully")

    if wav_file is None:
        logger.warning("error occurred while saving audio to data store")
        return None
    else:
        logger.info("about to process audio for STT ")
        import src.bot_service as bot_service
        bot_audio_response, text = bot_service.respond(wav_file)

        if bot_audio_response is None:
            logger.warning("error while responding to speech request")

        else:
            logger.info("request processing done and successful")
            # replace with server ip and port
            return jsonify(
                audio="http://localhost:5000/static/audio_response/response.wav",
                response_text="hello world",
                transcribed_text=text
            )


# run the application
if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)

# serve.py
import logging as logger
import logging.config
import time
import os
import system_paths

from waitress import serve
from flask import Flask, render_template, request, send_file, redirect


# creates a Flask application, named app
app = Flask(__name__)
app.config["DEBUG"] = True

# configure the logging format
logger.config.fileConfig(system_paths.resource + "/config/logger.conf")


# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    message = "Welcome to the beautiful experience"
    return render_template('index.html', message=message)


# the bot controller endpoint for all dialogue
@app.route("/c3p0", methods=["POST"])
def bot_controller():
    logger.info("about to process dialog audio")
    request_audio_wav = request.files['audio']

    # saving audio request to data store for processing
    import src.util.util as util
    wav_file = util.save_audio_request(request_audio_wav)

    if wav_file is None:
        logger.warning("error occurred while saving audio to data store")
        return None
    else:
        import src.bot_service as bot_service
        bot_audio_response = bot_service.respond(wav_file)

        if bot_audio_response is None:
            logger.warning("error while responding to speech request")

        else:
            logger.info("request processing done and successful")
            return send_file(bot_audio_response)


# run the application
if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)

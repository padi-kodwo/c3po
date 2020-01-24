# serve.py
import logging as logger
import logging.config
import time
import os

from waitress import serve
from flask import Flask, render_template, redirect, request, session


# creates a Flask application, named app
app = Flask(__name__)
app.config["DEBUG"] = True

# configure the logging format
logger.config.fileConfig(os.path.dirname(__file__) + "/resource/config/logger.conf")


# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    print(session)
    message = "The Flask Shop"
    return render_template('index.html', message=message)


# run the application
if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5000)

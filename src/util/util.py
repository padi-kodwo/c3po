import logging as logger
import logging.config
import os
from playsound import playsound

import system_paths

# configure the logging format
logger.config.fileConfig(system_paths.resource + "/config/logger.conf")


# saves audio file to the current file system
def save_audio_request(audio_wav):
    temp = "temp.wav"
    logger.info("audio file passed to saved")
    if audio_wav is None:
        logger.info("audio passed was null")
        return None
    else:
        logger.info("audio wave file about to be save")
        files_destination = os.path.join(system_paths.data_store, temp)
        audio_wav.save(files_destination)
        logger.info("done saving file to destination " + str(files_destination))
        return str(files_destination)


def play_audio(audio_path):
    playsound(audio_path)
    return
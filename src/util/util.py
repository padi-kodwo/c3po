import logging as logger
import logging.config
import os
import sys
import time

import system_paths


# saves audio file to the current file system
def save_audio_request(audio_wav):
    if audio_wav is None:
        logger.info("")
        return None
    elif not isinstance():
        logger.info("")
        return None
    else:
        files_destination = os.path.join(system_paths.data_store, audio_wav)
        audio_wav.save(files_destination)
        return files_destination

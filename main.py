import eel
import sys
import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import traceback
import platform
from app.utils import *
import os
import time

from vits.synthesizer import Synthesizer
from flask import Flask, request, send_file

synthesizer = Synthesizer(TTS_CONFIG_PATH)

if TTS_MODEL_PATH.exists():
   synthesizer.load_model(TTS_MODEL_PATH)
else:
   download_model("G_600000.pth")

synthesizer.load_model(TTS_MODEL_PATH)
synthesizer.init_speaker_map(SPEAKER_CONFIG)

app = Flask(__name__)


def remove_files():
 dir_path = r'tmp'
 treshold = time.time() - 3600
 for path in os.listdir(dir_path):
  if os.path.isfile(os.path.join(dir_path, path)):
     creation_time = os.stat(os.path.join(dir_path, path)).st_ctime
     if creation_time < treshold:
      os.remove(os.path.join(dir_path, path))
   
@app.route('/', methods=['GET'])
def tts():
    args = request.args
    # ImmutableMultiDict([('speaker', '1'), ('text', 'asdqwe')])
    
    params = { 
     "speech_var_a": 0.345, 
     "speech_var_b": 0.5,
     "speech_speed": 1.1
    }
    
    audio_data = synthesizer.synthesize(args.get('text'),args.get('speaker_id'),params)

    cur_timestamp = datetime.now().strftime("%m%d%f")
    tmp_path = Path("tmp")

    if not tmp_path.exists():
        tmp_path.mkdir()
    
    remove_files()
        
    file_name = "_".join(
        [str(cur_timestamp), "tmp_file"]
    )
    
    save_audio(tmp_path, file_name, audio_data)
    return send_file("../tmp/" + file_name + ".wav")

if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0") #host="0.0.0.0" will make the page accessable
                            #by going to http://[ip]:5000/ on any computer in 
                            #the network.

import eel
import sys
import json
from datetime import datetime
from pathlib import Path
import traceback
import platform
from app.utils import *
import os
import time
import hashlib

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


def remove_files(path):
 dir_path = path
 treshold = time.time() - 3600
 for path in os.listdir(dir_path):
  if os.path.isfile(os.path.join(dir_path, path)):
     creation_time = os.stat(os.path.join(dir_path, path)).st_ctime
     if creation_time < treshold:
      os.remove(os.path.join(dir_path, path))
   
@app.route('/', methods=['GET'])
def tts():
    args = request.args

    if args.get('text') is None:
      
      contents = "<h1>GameTTS Engine</h1>"
      contents = contents + "<p>This TTS service is based on the work of lexkoro, jaywalnut310 and the vits project. This neural network, which is able to imitate voices from well-known computer games, is published under CC-BY-NC 4.0. This server is a proof-of-concept and can be used free of charge. However, there is no claim to availability, or claim to quality when using this service.</p>"
      
      contents = contents + "<h2>Examples</h2>"
      contents = contents + "<li><a href='?speaker_id=48&text=Dieses ist ein Test.'>Gero Wachenholz saying: this is a test.</a></li>"
      contents = contents + "<li><a href='?speaker_id=26&text=Was sagt ein grosser Stift zu einem kleinen Stift? Wachs mal Stift.'>Uwe Koschel telling a joke.</a></li>"
      contents = contents + "<li><a href='?speaker_id=73&text=Guten Morgen.'>Boss Orc saying: Good Morning</a></li>"      
      
      contents = contents + "<h2>GET Parameters</h2>"      
      contents = contents + "<ul>"
      contents = contents + "<li>speaker_id - VoiceID from the List below</li>"
      contents = contents + "<li>text</li>"
      contents = contents + "</ul>"
      
      contents = contents + "<h2>Voices</h2>"
      
      c_json = Path("/usr/src/app/GameTTS/static_web/resource/json-mapping/game_speaker_map.json").read_text()
      json_ob = json.loads(c_json)
      
      for key in json_ob:
         contents = contents + "<h3>" + key + "</h3>"
         contents = contents + "<table border='1'>"
         contents = contents + "<tr><td>speaker_id</td><td>Speaker Name</td><td>Example</td></tr>"    
         for speaker in json_ob[key]:
            contents = contents + "<tr><td>" + json_ob[key][speaker] + "</td><td>" + speaker + "</td><td><a href='?speaker_id=" + json_ob[key][speaker] + "&text=Was sagt ein grosser Stift zu einem kleinen Stift Wachs mal Stift.'>Example</a></td></tr>"
         contents = contents + "</table>"
      return contents 
       
    else:

      params = { 
       "speech_var_a": 0.345, 
       "speech_var_b": 0.5,
       "speech_speed": 1.1
      }

      hashname = hashlib.md5(str(args.get('text') + args.get('speaker_id')).encode('utf-8')).hexdigest()
      tmp_path = "GameTTS/tmp/"
      file_name = tmp_path + hashname + ".wav"

      if not os.path.exists(tmp_path):
          os.mkdir(tmp_path)
    
      if not os.path.exists(file_name):
       print("file " + file_name + " not found")
       remove_files(tmp_path)
       audio_data = synthesizer.synthesize(args.get('text'),args.get('speaker_id'),params)
       save_audio(tmp_path, hashname, audio_data)
           
      return send_file("tmp/" + hashname + ".wav")

if __name__ == '__main__':
 app.debug = False
 app.run(host="0.0.0.0")

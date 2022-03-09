from flask import Flask, request, send_file
import requests
from flask_cors import CORS
from dotenv import load_dotenv
from time import sleep, time
import os
import json

file_prefix = os.path.dirname(__file__)

try:
    from model_lyrics.run import run
    from model_lyrics.runGPT2 import gen_gpt2
    from model_beats.test import main_test
    from utils import *
except:
    from .model_lyrics.run import run
    from .model_lyrics.runGPT2 import gen_gpt2
    from .model_beats.test import main_test
    from .utils import *   

load_dotenv()

# instantiate the app
app = Flask(__name__, static_folder='../client/dist/', static_url_path='/')
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/lyrics_weights')
def lyrics_weights():
    args = request.args
    portion = args.get('portion')

    print("Start weight download")
    #download_from_drive(lyric_model_keys.get(portion), "model_lyrics/save.data-00000-of-00001", portion == "0")
    download_from_drive(lyric_model_key, "model_lyrics/save.data-00000-of-00001", True)
    print("Finish weight download")

    if not os.path.exists(os.path.join(file_prefix, "model_lyrics/gpt2-model/")):
        os.makedirs(os.path.join(file_prefix, "model_lyrics/gpt2-model/"))

    print("Start GPT2 download")
    for i in range(len(gpt2_keys)):
        print("Start downloading file", gpt2_names[i])
        download_from_drive(gpt2_keys[i], "model_lyrics/gpt2-model/" + gpt2_names[i], True)
    print("Finish GPT2 download")
    return "ok"

@app.route('/new_lyrics')
def generate_lyrics():
    args = request.args
    seed = args.get('seed')
    length = args.get('length')

    print(seed)
    if (len(seed) > 0):
        if (len(length) > 0):
            #seed_word = seed.split()[0]
            result = gen_gpt2(seed=seed, output_len=int(length))
        else:
            result = gen_gpt2(seed=seed)
            #seed_word = ""
    else:
        if (len(length) > 0):
            result = gen_gpt2(output_len=int(length))
        else:
            result = gen_gpt2()

    return result
    #return run(seed_word)

@app.route('/new_beat')
def generate_beat():
    args = request.args
    length = args.get('length')

    return main_test(length=int(length))

@app.route('/midi')
def return_midi():
    args = request.args
    src = args.get('src')

    midi = open(os.path.join(file_prefix, 'model_beats', 'outputs', src), 'rb')
    return send_file(midi, mimetype='audio/midi')

@app.route('/wav')
def return_wav():
    args = request.args
    src = args.get('src')

    midi = open(os.path.join(file_prefix, 'tts', src), 'rb')
    return send_file(midi, mimetype='audio/wav')

@app.route('/tts')
def generate_tts():
    args = request.args
    text = args.get('text')
    voice = args.get('voice')

    # generate body
    body = {
        "speech": text,
        "voice": voice
    }

    # Auth header
    headers = {
        "Authorization": "Basic cHViX2V1cGV0Zm5heGt4b3hwY3ZiYTpwa19jMzRmZDAwZi04YjljLTQ0ZjEtYThhZi00ZmZhYzYwYjZmZGM="
    }

    # Send request to uberduck and indicate it has not been processed yet
    response = requests.post("https://api.uberduck.ai/speak", data=json.dumps(body), headers=headers)
    processed = False
    parsed = json.loads(response.content.decode('utf-8'))
    uuid = parsed['uuid']

    if not os.path.exists(os.path.join(file_prefix, "tts/")):
        os.makedirs(os.path.join(file_prefix, "tts/"))

    requested_time = time()
    while not processed:
        sleep(10)
        response = requests.get("https://api.uberduck.ai/speak-status?uuid=" + uuid, headers=headers)
        parsed = json.loads(response.content.decode('utf-8'))
        if parsed['path'] != None:
            processed = True
            wav_bytes = requests.get(parsed['path'])

            with open(os.path.join(file_prefix, "tts", str(requested_time) + '.wav'), "wb") as file:
                file.write(wav_bytes.content)

    return str(requested_time) + '.wav'



@app.route('/snoop')
def snoop():
    return 'ok'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

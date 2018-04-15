import regex
import requests
import subprocess
import sys
import json

from flask import render_template, request

from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.dict import Cedict
from CJKhyperradicals.frequency import ChineseFrequency, JapaneseFrequency
from CJKhyperradicals.variant import Variant
from CJKhyperradicals.tts import Tts
from CJKhyperradicals.sentence import jukuu, wwwjdic

from webview import app

decompose = Decompose()
variant = Variant()
cedict = Cedict()
zh_sorter = ChineseFrequency()
ja_sorter = JapaneseFrequency()

server_values = {
    'language': 'zh',
    'currentChar': ' '
}


@app.route('/', methods=['GET', 'POST'])
def index():
    global server_values

    if request.method == 'POST':
        data = request.form
        if 'sentence' in data.keys():
            server_values['characters'] = regex.sub(r'[^\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]',
                                                    '', data['sentence'])
            server_values['charNumber'] = 0

            if server_values['characters']:
                server_values['currentChar'] = server_values['characters'][server_values['charNumber']]
        elif 'charNumber' in data.keys():
            server_values['charNumber'] += int(data['charNumber'])
            server_values['currentChar'] = server_values['characters'][server_values['charNumber']]
        elif 'character' in data.keys():
            server_values['currentChar'] = data['character']
            server_values['characters'] = data['character'][0]
            server_values['charNumber'] = 0
        elif 'language' in data.keys():
            server_values['language'] = data['language']

        sorter = {
            'ja': ja_sorter,
            'zh': zh_sorter
        }.get(server_values['language'], zh_sorter)

        if server_values['language'] == 'zh':
            vocab = sorter.sort_vocab([list(item) for item in cedict.search_hanzi(server_values['currentChar'])])[:10]
            sentences = list(jukuu(server_values['currentChar']))
        elif server_values['language'] == 'ja':
            vocab = requests.get('http://beta.jisho.org/api/v1/search/words?keyword='
                                 + server_values['currentChar']).json()
            sentences = list(wwwjdic(server_values['currentChar']))
        else:
            vocab = []
            sentences = []

        return json.dumps({
            'characters': server_values['characters'],
            'charNumber': server_values['charNumber'],
            'currentChar': server_values['currentChar'],
            'language': server_values['language'],
            'compositions': decompose.get_sub(server_values['currentChar']),
            'supercompositions': sorter.sort_char(decompose.get_super(server_values['currentChar'])),
            'variants': variant.get(server_values['currentChar']),
            'vocab': vocab,
            'sentences': sentences
        })

    return render_template('index.html', defaultValue=server_values)


@app.route('/speak', methods=['POST'])
def speak():
    if request.method == 'POST':
        if request.url_root == 'http://127.0.0.1:5050/' and sys.platform == 'darwin':
        # if False:
            speaker = {
                'zh-CN': 'ting-ting',
                'ja': 'kyoko'
            }.get(request.form['lang'])
            subprocess.Popen(['say', '-v', speaker, request.form['vocab']])
            return ""
        else:
            return Tts(request.form['vocab'], request.form['lang']).to_bytes()

    return ""

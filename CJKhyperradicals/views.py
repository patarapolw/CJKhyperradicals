import regex
import requests

from flask import render_template, request, send_from_directory

from CJKhyperradicals import app
from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.dict import Cedict
from CJKhyperradicals.frequency import ChineseFrequency, JapaneseFrequency
from CJKhyperradicals.variant import Variant
from CJKhyperradicals.speak import client_say

decompose = Decompose()
variant = Variant()
cedict = Cedict()
# edict2 = Edict2()
zh_sorter = ChineseFrequency()
ja_sorter = JapaneseFrequency()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        sorter = {
            'ja': ja_sorter,
            'zh': zh_sorter
        }.get(data['language'], zh_sorter)

        if data['sentence'].isdigit():
            char_to_read = data['sentence']
            characters = char_to_read
            char_number = 0
        else:
            characters = regex.sub(r'[^\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]', '',
                                   data['sentence'])
            char_number = int(data['char-number'])
            if char_number >= len(characters):
                char_number = 0
            if characters:
                char_to_read = characters[char_number]
            else:
                char_to_read = ''
        if characters:
            if data['language'] == 'zh':
                vocab = sorter.sort_vocab([list(item) for item in cedict.search_hanzi(char_to_read)])
            elif data['language'] == 'ja':
                # vocab = edict2.search_kanji(char_to_read)  # Japanese vocab sorter needs to be implemented.
                vocab = requests.get('http://beta.jisho.org/api/v1/search/words?keyword=' + char_to_read).text
            else:
                vocab = []

            params = {
                'characters': characters,
                'lang': data['language'],
                'charNumber': char_number,
                'compositions': decompose.get_sub(char_to_read),
                'supercompositions': sorter.sort_char(decompose.get_super(char_to_read)),
                'variants': variant.get(char_to_read),
                'vocab': vocab
            }
        else:
            params = dict()
        return render_template('index.html', **params)
    else:
        return render_template('index.html')


@app.route('/speak', methods=['POST'])
def speak():
    if request.method == 'POST':
        # speaker = {
        #     'zh-CN': 'ting-ting',
        #     'ja': 'kyoko'
        # }.get(request.form['lang'])
        # subprocess.Popen(['say', '-v', speaker, request.form['vocab']])

        return send_from_directory('tmp', client_say(request.form['vocab'], request.form['lang']))

    return ""

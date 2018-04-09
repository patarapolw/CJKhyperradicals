import requests
from bs4 import BeautifulSoup
import json
import os


def get_joyo():
    data = dict()
    r = requests.get('https://en.wikipedia.org/wiki/List_of_jōyō_kanji')
    soup = BeautifulSoup(r.text, 'html.parser')
    for tr in soup.find_all('table')[1].find_all('tr'):
        td = tr.find_all('td')
        if td:
            grade = td[5].text
            kanji = td[1].text[0]
            data[grade] = data.get(grade, '') + kanji

    return data


def get_common(limit=2500,
               sources=('aozora.json', 'news.json', 'twitter.json', 'wikipedia.json')):
    all_chars = dict()
    for source in sources:
        with open(os.path.join('frequency', source)) as f:
            for i, row in enumerate(json.load(f)):
                if 0 < i <= limit:
                    all_chars.setdefault(row[0], []).append(i)

    return sorted(all_chars.keys(), key=lambda x: max(all_chars[x]))


if __name__ == '__main__':
    joyo = get_joyo()
    extra = ''
    for common in get_common():
        if common not in ''.join(joyo.values()):
            extra += common
    joyo['extra'] = extra

    with open('frequency.json', 'w') as f:
        json.dump(joyo, f, ensure_ascii=False, indent=2, sort_keys=True)

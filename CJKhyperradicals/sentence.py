import requests
from bs4 import BeautifulSoup


def jukuu(vocab):
    params = {
        'q': vocab
    }
    r = requests.get('http://www.jukuu.com/search.php', params=params)
    soup = BeautifulSoup(r.text, 'html.parser')

    return zip([c.text for c in soup.find_all('tr', {'class': 'c'})],
               [e.text for e in soup.find_all('tr', {'class': 'e'})])


def wwwjdic(vocab, limit=20):
    data = {
        "exsrchstr": vocab,
        "exsrchnum": limit
    }
    r = requests.post('http://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?11', data=data)
    soup = BeautifulSoup(r.text, 'html.parser')

    for li in soup.find_all('li'):
        contents = li.text.strip().split('\n')
        yield contents[0], contents[2]


if __name__ == '__main__':
    # print(list(jukuu('你好')))
    print(list(wwwjdic('おはよう')))

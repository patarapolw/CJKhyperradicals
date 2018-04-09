import re

from CJKhyperradicals.dir import chinese_path, japanese_path


class Cedict:
    def __init__(self):
        self.entries = set()
        with open(chinese_path('cedict_ts.u8')) as f:
            for row in f:
                _ = re.match(r'([^ ]+) ([^ ]+) \[(.+)\] /(.+)/', row)
                if _ is not None:
                    # trad, simp, pinyin, english = _.groups()
                    self.entries.add(_.groups())
                else:
                    # print(row)
                    pass

    def search_hanzi(self, hanzi):
        for entry in self.entries:
            if hanzi in (entry[0] + entry[1]):
                yield entry

    def search_vocab(self, vocab):
        for entry in self.entries:
            if vocab in (entry[0], entry[1]):
                yield entry


class Edict2:
    def __init__(self):
        self.entries = set()
        with open(japanese_path('edict2'), encoding='euc-jp') as f:
            for row in f:
                _ = re.match(r'([^ ]+) \[(.+)\] /(.+)/', row)
                if _ is not None:
                    self.entries.add(_.groups())
                else:
                    _ = re.match(r'([^ ]+) /(.+)/', row)
                    if _ is not None:
                        kana, meaning = _.groups()
                        self.entries.add((kana, kana, meaning))
                    else:
                        raise ValueError(row + "not read.")

    def search_kanji(self, kanji):
        for entry in self.entries:
            if kanji in entry[0]:
                yield entry


if __name__ == '__main__':
    # print(Edict2().entries)
    pass

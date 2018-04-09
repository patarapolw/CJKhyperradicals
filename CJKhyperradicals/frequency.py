import math
import json
from wordfreq import word_frequency

from CJKhyperradicals.dir import chinese_path, japanese_path


class ChineseFrequency:
    def __init__(self):
        self.sequence = []
        with open(chinese_path('junda.txt')) as f:
            for row in f:
                contents = row.split('\t')
                self.sequence.append(contents[1])

    def sort_char(self, hanzi_list, limit=5000):
        return sorted([hanzi for hanzi in hanzi_list if self.freq_char(hanzi) <= limit], key=self.freq_char)

    def freq_char(self, hanzi):
        try:
            return self.sequence.index(hanzi)
        except ValueError:
            return math.inf

    def sort_vocab(self, vocab_tuple_list):
        return sorted([vocab_tuple for vocab_tuple in vocab_tuple_list],
                      key=lambda x : self.freq_vocab(x[1]), reverse=True)

    @staticmethod
    def freq_vocab(vocab):
        return word_frequency(vocab, 'zh')


class JapaneseFrequency:
    def __init__(self):
        with open(japanese_path('frequency.json')) as f:
            self.entries = json.load(f)

    def sort_char(self, kanji_list):
        return sorted([kanji for kanji in kanji_list if self.freq_char(kanji) is not None],
                      key=lambda x: self.freq_char(x))

    def freq_char(self, kanji):
        for k, v in self.entries.items():
            if kanji in v:
                return k, v.index(kanji)

        return None

    # def sort_vocab(self, vocab_tuple_list):
    #     return sorted([vocab_tuple for vocab_tuple in vocab_tuple_list],
    #                   key=lambda x : self.freq_vocab(x[1]), reverse=True)
    #
    # @staticmethod
    # def freq_vocab(vocab):
    #     return word_frequency(vocab, 'ja')


if __name__ == '__main__':
    # print(word_frequency('おはよう', 'ja'))
    pass

#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

__version__ = '0.9'
__all__ = ["PinYin"]

import os.path

PINYIN_DIR = os.path.abspath(os.path.dirname(__file__))


class PinYin(object):
    def __init__(self, dict_file='word.data'):
        self.word_dict = {}
        self.dict_file = os.path.join(PINYIN_DIR, dict_file)
        self._load_word()

    def _load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with file(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('	')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]

    def _hanzi2pinyin(self, words=""):
        result = []
        if not isinstance(words, unicode):
            words = words.decode("utf-8")

        for char in words:
            key = '%X' % ord(char)
            tmp = self.word_dict.get(key, char).split()
            if tmp:
                #print tmp
                result.append(tmp[0][:-1].lower())
        return result

    def getpinyin(self, words, spot=','):
        result = self._hanzi2pinyin(words.replace(" ", ""))
        if not result:
            return ['', '']
        jp = "".join([each[0] for each in result if each])
        qp = spot.join(each for each in result if each)
        return [jp, qp]

    def getpinyin2(self, words, spot=','):
        result = self._hanzi2pinyin(words.replace(" ", ""))
        if not result:
            return []
        return spot.join(each for each in result if each)


def get_quanpin(text, spot=','):
    py_obj = PinYin()
    return py_obj.getpinyin2(text, spot)


def get_pinyin(text, spot=','):
    py_obj = PinYin()
    return py_obj.getpinyin(text, spot)


if __name__ == "__main__":
    ## 这里只获得汉字的全拼，
    test = PinYin()
    words = "叶"
    arr = test.getpinyin2(words)
    jp = arr[0]
    qp = arr[1]
    print "%s 简拼：%s 全拼：%s" %(words, jp, qp)


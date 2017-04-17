# coding=UTF-8
import requests
from bs4 import BeautifulSoup

class BookCollection():
    result = {'title':'', 'author':'', 'ISBN':'', 'publisher':''
    , 'edition':'', 'page':''}

    def __init__(self, sourceCode):
        sourceCode = self.setFullBookDetail(sourceCode)
        self.setResiltDict(sourceCode)

    def setFullBookDetail(self, sourceCode):
        parser = sourceCode.find(class_ = 'bibInfoEntry')
        parser = parser.stripped_strings
        return parser

    def setResiltDict(self, sourceCode):
        class_ = {'著者':'author', '題名':'title', '版本項':'edition'
        , '出版項':'publisher', '面數高廣':'page', '國際標準書號':'ISBN'}
        for i in sourceCode:
            if self.isClass(i):
                targetClass = class_[i]
                continue
            if targetClass == 'title':
                parser = i.split(' / ')
                self.result['title'] = parser[0]
                self.result['author'] = parser[1]
                continue
            self.result[targetClass] += i

    def isClass(self, text):
        class_ = ['著者', '題名', '版本項', '出版項', '面數高廣', '國際標準書號']
        for i in class_:
            if text == i:
                return True
        return False

# Demo
if __name__ == '__main__':
    print("Run demo")
    isbn = 9789860516098
    data = BookCollection(isbn)

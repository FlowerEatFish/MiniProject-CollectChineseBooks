# coding=UTF-8
import requests
from bs4 import BeautifulSoup

class BookDetail():
    result = {'name':'', 'author':'', 'ISBN':'', 'publisher':'', 'pub_year':'', 'edition':''}
    
    def __init__(self, isbn):
        sourceCode = self.getFilterSourceCode(isbn)
        self.result['name'] = self.getName(sourceCode)
        self.result['author'] = self.getAuthor(sourceCode)
        print(self.result)

    def isIsbn(self, isbn):
        if type(isbn) is int:
            return True
        return False

    def getFilterSourceCode(self, isbn):
        url = 'http://nbinet3.ncl.edu.tw/search*cht/i?SEARCH=%d+&searchscope=1' % isbn
        print(url)
        browser = 'Chrome/55.0.2924.87'
        header = {'user-agent' : browser}
        resource = requests.get(url, headers = header)
        sourceCode = BeautifulSoup(resource.text, 'html.parser')
        print(sourceCode.prettify())
        return sourceCode.find(class_ = 'bibMain')
        
    def getName(self, sourceCode):
        filter_ = sourceCode.find(class_ = 'bibInfoData')
        filter_ = sourceCode.find('strong')
        text = filter_.string.split(" / ")
        return text[0]

    def getAuthor(self, sourceCode):
        filter_ = sourceCode.find(class_ = 'bibInfoData')
        filter_ = sourceCode.find('strong')
        text = filter_.string.split(" / ")
        return text[1]

# Demo
if __name__ == '__main__':
    print("Run demo")
    isbn = 9789860516098
    data = BookDetail(isbn)

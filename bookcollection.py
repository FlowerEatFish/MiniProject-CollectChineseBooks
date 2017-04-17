# coding=UTF-8
import requests
from bs4 import BeautifulSoup

class BookCollection():
    result = {'name': '', 'author': '', 'ISBN': '', 'publisher': '', 'pub_year': '', 'edition': ''}

    def __init__(self, sourceCode):
        sourceCode = self.setFullBookDetail(sourceCode)
        self.result['name'] = self.getName(sourceCode)
        self.result['author'] = self.getAuthor(sourceCode)
        self.result['ISBN'] = self.getISBN(sourceCode)
        self.result['publisher'] = self.getpublisher(sourceCode)
        self.result['pub_year'] = self.getPubYear(sourceCode)
        self.result['edition'] = self.getEdition(sourceCode)

    def setFullBookDetail(self, sourceCode):
        parser = sourceCode.find_all(class_ = 'bibInfoData')
        return parser

    def getName(self, sourceCodeList):
        result = sourceCodeList[0].find('strong')
        result = result.string.split(' / ')
        return result[0]

    def getAuthor(self, sourceCodeList):
        result = sourceCodeList[0].find('strong')
        result = result.string.split(' / ')
        return result[1]

    def getpublisher(self, sourceCodeList):
        result = sourceCodeList[3]
        result = result.find('a')
        return result.string

    def getEdition(self, sourceCodeList):
        result = sourceCodeList[1]
        return result.string

    def getISBN(self, sourceCodeList):
        result = sourceCodeList[5]
        return result.string

    def getPubYear(self, sourceCodeList):
        result = sourceCodeList[2]
        return result.string

# Demo
if __name__ == '__main__':
    print("Run demo")
    isbn = 9789860516098
    data = BookCollection(isbn)

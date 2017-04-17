# coding=UTF-8
import requests
from bs4 import BeautifulSoup

class SimpleParser():
    layerCheckList = ['browseEntry', 'browseSuperEntry', 'bibMain']
    data = ''
    # browseEntry - First Layer
    # browseSuperEntry - Second Layer
    # bibMain - Third Layer

    def __init__ (self, isbn):
        url = 'http://nbinet3.ncl.edu.tw/search*cht/i?SEARCH=%d+&searchscope=1' % isbn
        print('Layer 1: %s' % url)
        sourceCode = self.getFilterSourceCode(url)
        bookLayer = self.setLayer(sourceCode)
        if bookLayer == 'browseEntry':
            url = self.setFirstTargetUrl(sourceCode)
            print('Layer 2: %s' % url)
            sourceCode = self.getFilterSourceCode(url)
            bookLayer = self.setLayer(sourceCode)
        if bookLayer == 'browseSuperEntry':
            url = self.setSecondTargetUrl(sourceCode)
            print('Layer 3: %s' % url)
            sourceCode = self.getFilterSourceCode(url)
            bookLayer = self.setLayer(sourceCode)
        self.data = sourceCode

    def getFilterSourceCode(self, url):
        browser = 'Chrome/55.0.2924.87'
        header = {'user-agent': browser}
        resource = requests.get(url, headers = header)
        sourceCode = BeautifulSoup(resource.text, 'html.parser')
        return sourceCode

    def setLayer(self, sourceCode):
        for i in self.layerCheckList:
            if sourceCode.prettify().find('%s' % i) > -1:
                return i
        return None

    def setFirstTargetUrl(self, sourceCode):
        result = sourceCode.find(class_ = 'browseEntryData')
        result = result.find_all('a')
        result = result[1]['href']
        return 'http://nbinet3.ncl.edu.tw%s' % result

    def setSecondTargetUrl(self, sourceCode):
        result = sourceCode.find(class_ = 'briefcitTitle')
        result = result.find('a')
        result = result['href']
        return 'http://nbinet3.ncl.edu.tw%s' % result

# Demo
if __name__ == '__main__':
    print("Run demo")
    isbn = 9789861943107
    data = SimpleParser(isbn)

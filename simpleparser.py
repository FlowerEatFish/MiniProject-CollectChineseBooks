# coding=UTF-8
import requests
from bs4 import BeautifulSoup

class SimpleParser():
    layerCheckList = ['browseEntry','browseSuperEntry','bibMain']
    libraryList = ['淡江大學','成功大學','臺北市立圖書','國家圖書','新書書訊']
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
            url = self.getFirstLayerData(sourceCode)
            #url = self.setFirstTargetUrl(sourceCode)
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

    # First Layer Domain
    def getFirstLayerData(self, sourceCode):
        data = self.setDataList(sourceCode)
        data = self.setDataAllUrl(sourceCode, data)
        data = self.setDataAllLibrary(sourceCode, data)
        return data[0]['url']

    def setDataList(self, sourceCode):
        temp = {'url': None, 'library': []}
        sourceCode_string = sourceCode.prettify()
        count = sourceCode_string.count('browseEntryData')
        data = [temp]*count
        return data

    def setDataAllUrl(self, sourceCode, data):
        parser = sourceCode.find_all(class_ = 'browseEntryData')
        for i in range(len(data)):
            result = parser[i].find_all('a')
            result = result[1]['href']
            result = 'http://nbinet3.ncl.edu.tw%s' % result
            data[i]['url'] = result
        return data

    def setDataAllLibrary(self, sourceCode, data):
        # set temp_index_Data
        temp_index_Data = []
        index = 0
        while index < len(sourceCode):
            index = sourceCode.prettify().find('browseEntryData', index)
            print("browseEntryData:%d" % index)
            if index == -1:
                break
            temp_index_Data.append(index)

        # set temp_index_SubData
        temp_index_SubData = []
        index = 0
        while index < len(sourceCode):
            index = sourceCode.prettify().find('browseSubEntryData')
            print("browseSubEntryData:%d" % index)
            if index == -1:
                break
            temp_index_SubData.append(index)

        # set Library
        temp_library = sourceCode.find_all(class_ = 'browseSubEntryData')
        print(len(temp_library), len(temp_index_SubData))
        for i in range(len(temp_library)):
            targetLibrary = temp_library[i].find('strong').get_text()
            print(targetLibrary)
            targetDataIndex = 0
            for j in range(len(temp_index_Data)):
                if temp_index_SubData[i] > temp_index_Data[j]:
                    targetDataIndex = j
                    print(data[j]['library'])
                    data[j]['library'].append(targetLibrary)
        return data

    def setFirstTargetUrl(self, sourceCode):
        result = sourceCode.find(class_ = 'browseEntryData')
        result = result.find_all('a')
        result = result[1]['href']
        return 'http://nbinet3.ncl.edu.tw%s' % result

	# Second Layer Domain
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

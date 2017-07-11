# coding=UTF-8
import requests
from bs4 import BeautifulSoup

class SimpleParser():
    layerCheckList = ['browseEntry','browseSuperEntry','bibMain']
    # browseEntry - First Layer
    # browseSuperEntry - Second Layer
    # bibMain - Third Layer
    libraryList = ['淡江大學','成功大學','臺北市立圖書','國家圖書','新書書訊']
    data = ''

    def __init__ (self, isbn):
        url = 'http://nbinet3.ncl.edu.tw/search*cht/i?SEARCH=%d+&searchscope=1' % isbn
        print('Layer 1:\n%s' % url)
        sourceCode = self.getFilterSourceCode(url)
        bookLayer = self.setLayer(sourceCode, self.layerCheckList)

        if self.isFileNotFound(sourceCode):
            print('%d: File no found.' % isbn)
            self.data = ''
        else:
            if bookLayer == 'browseEntry':
                url = self.getFirstLayerData(sourceCode)
                print('Layer 2:\n%s' % url)
                sourceCode = self.getFilterSourceCode(url)
                bookLayer = self.setLayer(sourceCode, self.layerCheckList)
            if bookLayer == 'browseSuperEntry':
                url = self.getSecondLayerData(sourceCode)
                print('Layer 3:\n%s' % url)
                sourceCode = self.getFilterSourceCode(url)
                bookLayer = self.setLayer(sourceCode, self.layerCheckList)
            self.data = sourceCode

    def getFilterSourceCode(self, url):
        browser = 'Chrome/55.0.2924.87'
        header = {'user-agent': browser}
        resource = requests.get(url, headers = header)
        sourceCode = BeautifulSoup(resource.text, 'html.parser')
        return sourceCode

    def setLayer(self, sourceCode, layerCheckList):
        for i in layerCheckList:
            if sourceCode.prettify().find('%s' % i) > -1:
                return i
        return None

    # if file no found
    def isFileNotFound(self, sourceCode):
        stringSourceCode = sourceCode.get_text()
        if stringSourceCode.find('沒有查獲符合查詢條件的館藏') != -1:
            return True
        return False

    # --- First Layer Domain | Start ---
    def getFirstLayerData(self, sourceCode):
        data = self.setDataList(sourceCode, 'browseEntryData')
        data = self.setFirstDataAllUrl(sourceCode, data)
        data = self.setFirstDataAllLibrary(sourceCode, data)
        #print('Layer 1 data:\n%s' % str(data))
        result = self.getTargetLibrary(data, self.libraryList)
        return result

    def setFirstDataAllUrl(self, sourceCode, data):
        parser = sourceCode.find_all(class_ = 'browseEntryData')
        for i in range(len(data)):
            result = parser[i].find_all('a')
            result = result[1]['href']
            result = 'http://nbinet3.ncl.edu.tw%s' % result
            data[i]['url'] = result
        return data

    def setFirstDataAllLibrary(self, sourceCode, data):
        # set temp_index_Data
        temp_index_Data = []
        index = 0
        while index < len(sourceCode.prettify()):
            index = sourceCode.prettify().find('browseEntryData', index)
            if index == -1:
                break
            temp_index_Data.append(index)
            index += 15

        # set temp_index_SubData
        temp_index_SubData = []
        index = 0
        while index < len(sourceCode.prettify()):
            index = sourceCode.prettify().find('browseSubEntryData', index)
            if index == -1:
                break
            temp_index_SubData.append(index)
            index += 18

        # set Library
        temp_library = sourceCode.find_all(class_ = 'browseSubEntryData')
        for i in range(len(temp_index_SubData)):
            try:
                targetLibrary = temp_library[i].find('strong').get_text()
                targetDataIndex = 0
                for j in range(len(temp_index_Data)):
                    if temp_index_SubData[i] > temp_index_Data[j]:
                        targetDataIndex = j
                        data[targetDataIndex]['library'].append(targetLibrary)
            except:
                continue
        return data
	# --- First Layer Domain | End ---

	# --- Second Layer Domain | Start ---
    def getSecondLayerData(self, sourceCode):
        data = self.setDataList(sourceCode, 'briefCitRow')
        data = self.setSecondDataAllUrl(sourceCode, data)
        data = self.setSecondDataAllLibrary(sourceCode, data)
        #print('Layer 2 data:\n%s' % str(data))
        result = self.getTargetLibrary(data, self.libraryList)
        return result

    def setSecondDataAllUrl(self, sourceCode, data):
        parser = sourceCode.find_all(class_ = 'briefcitTitle')
        for i in range(len(data)):
            result = parser[i].find_all('a')
            result = result[0]['href']
            result = 'http://nbinet3.ncl.edu.tw%s' % result
            data[i]['url'] = result
        return data

    def setSecondDataAllLibrary(self, sourceCode, data):
        parser = sourceCode.find_all(class_ = 'briefcitStatus')
        for i in range(len(data)):
            result = parser[i].get_text()
            data[i]['library'] = result
        return data
	# --- Second Layer Domain | End ---

	# --- First & Second Layer Domain | Start ---
    def setDataList(self, sourceCode, targetClassName):
        data = []
        sourceCode_string = sourceCode.prettify()
        count = sourceCode_string.count(targetClassName)
        for i in range(count):
            temp = {'url': None, 'library': []}
            data.append(temp)
        return data

    def getTargetLibrary(self, data, libraryList):
        for j in libraryList:
            for i in data:
                temp = str(i['library'])
                if temp.find(j) > 0:
		    		# if library includes in libraryList.
                    return i['url']
		# if no library includes in libraryList.
        return data[0]['url']

# Demo
if __name__ == '__main__':
    print("Run demo")
    isbn = 9789861943107
    data = SimpleParser(isbn)

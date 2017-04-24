import requests
from bs4 import BeautifulSoup

class Book():
    title = None
    author = None
    isbn = None
    publisher = None
    edition = None
    page = None
    price = None
    package = None

    def __init__(self, sourceCode):
        sourceCode = self.getFullBookDetail(sourceCode)
        self.setBookDetailTemplate(sourceCode)

    def getSourceCode(self, url):
        browser = 'Chrome/55.0.2924.87'
        header = {'user-agent': browser}
        resource = requests.get(url, headers = header)
        sourceCode = BeautifulSoup(resource.text, 'html.parser')
        return sourceCode

    def getFullBookDetail(self, sourceCode):
        parser = sourceCode.find(class_ = 'bibInfoEntry')
        parser = parser.stripped_strings
        return parser

    def setBookDetailTemplate(self, sourceCode):
        class_ = {'題名':'title_author', '版本項':'edition'
        , '出版項':'publisher', '面數高廣':'page', '國際標準書號':'isbn_package_price'}
        targetClass = None
        for i in sourceCode:
            if self.isClass(i, class_):
                targetClass = class_[i]
            else:
                self.setBookDetail(i, targetClass)

    def isClass(self, text, class_):
        for i in class_:
            if text == i:
                return True
        return False

    def setBookDetail(self, text, targetClass):
        if targetClass == 'title_author':
            parser = text.split(' / ')
            self.title = parser[0]
            self.author = parser[1]
        if targetClass == 'edition':
            self.edition = text
        if targetClass == 'publisher':
            self.publisher = text
        if targetClass == 'page':
            self.page = text
        if targetClass == 'isbn_package_price':
            print(text)
            parser = text.split(' ')
            self.isbn = parser[0]
            for i in parser:
                if i.find('平裝') != -1:
                    self.package = 'paperback'
                if i.find('精裝') != -1:
                    self.package = 'hardback'
                if i.find('NT') != -1:
                    self.price = i
                if i.find('幣') != -1:
                    self.price = i

if __name__ == '__main__':
    print('Run demo')
    url = 'http://nbinet3.ncl.edu.tw/search~S10*cht?/i9789865918187+/i9789865918187/1%2C2%2C8%2CE/frameset&FF=i9789865918187&1%2C%2C5'
    data = Book(url)
    print(data.title)
    print(data.author)
    print(data.publisher)
    print(data.edition)
    print(data.page)
    print(data.isbn)
    print(data.package)
    print(data.price)

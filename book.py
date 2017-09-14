""" Crawler libraries. """
import requests
from bs4 import BeautifulSoup

class Book():
    """ Parse book information from target website. """
    title = None
    author = None
    isbn = None
    publisher = None
    edition = None
    page = None
    price = None
    package = None

    def __init__(self, source_code):
        source_code = self.get_full_book_detail(source_code)
        self.set_book_detail_template(source_code)

    @staticmethod
    def get_source_code(url):
        """ Set header """
        browser = 'Chrome/55.0.2924.87'
        header = {'user-agent': browser}
        resource = requests.get(url, headers=header)
        source_code = BeautifulSoup(resource.text, 'html.parser')
        return source_code

    @staticmethod
    def get_full_book_detail(source_code):
        """ Find/set all details. Return string. """
        parser = source_code.find(class_='bibInfoEntry')
        parser = parser.stripped_strings
        return parser

    def set_book_detail_template(self, source_code):
        """ Set detail template for parse class on chinese language. """
        class_ = {'題名':'title_author', '版本項':'edition',
                  '出版項':'publisher', '面數高廣':'page', '國際標準書號':'isbn_package_price'}
        target_class = None
        for i in source_code:
            if self.is_class(i, class_):
                target_class = class_[i]
            else:
                self.set_book_detail(i, target_class)

    @staticmethod
    def is_class(text, class_):
        """ Check whether target class is included in class template. """
        for i in class_:
            if text == i:
                return True
        return False

    def set_book_detail(self, text, target_class):
        """ Collect detail follow class. """
        if target_class == 'title_author':
            parser = text.split(' / ')
            if len(parser) > 1:
                self.title = parser[0]
                self.author = parser[1]
            else:
                self.title = parser[0]
                self.author = 'none'
        if target_class == 'edition':
            self.edition = text
        if target_class == 'publisher':
            self.publisher = text
        if target_class == 'page':
            self.page = text
        if target_class == 'isbn_package_price':
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
    CHECK_URL = 'http://nbinet3.ncl.edu.tw/search~S10*cht?/i9789865918187+/i9789865918187/1%2C2%2C8%2CE/frameset&FF=i9789865918187&1%2C%2C5'
    DATA = Book(CHECK_URL)
    print(DATA.title)
    print(DATA.author)
    print(DATA.publisher)
    print(DATA.edition)
    print(DATA.page)
    print(DATA.isbn)
    print(DATA.package)
    print(DATA.price)

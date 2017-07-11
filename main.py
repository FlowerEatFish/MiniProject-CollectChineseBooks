# coding=UTF-8
from simpleparser import *
from read import *
from book import *
import write
import time

isbn = IsbnCollection()
database = []

for i in isbn.isbnList:
    if type(i) is int:
        parser = SimpleParser(i)
        if parser.data == '':
            continue
        else:
            data = Book(parser.data)
            database.append(data)
        time.sleep(3)

write.ExportResult(database)

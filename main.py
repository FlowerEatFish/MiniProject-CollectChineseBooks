# coding=UTF-8
from simpleparser import *
from read import *
from bookcollection import *
import time

isbn = IsbnCollection()

for i in isbn.isbnList:
    if type(i) is int:
        parser = SimpleParser(i)
        data = BookCollection(parser.data)
        print(data.result)
        time.sleep(10)

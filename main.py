# coding=UTF-8
from simpleparser import *
from bookcollection import *

isbn = 9789861943107
parser = SimpleParser(isbn)
data = BookCollection(parser.data)

print(data.result)

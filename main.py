# coding=UTF-8
from simpleparser import *
from bookcollection import *

parser = SimpleParser(isbn)
data = BookCollection(parser.data)

print(data.result)

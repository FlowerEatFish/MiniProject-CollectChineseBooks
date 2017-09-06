# coding=UTF-8
from simpleparser import *
from read import *
from book import *
import write
import time
import re

def isIntType(value):
    try:
        int(value)
        return True
    except:
        return False

isbn = IsbnCollection()
database = []

for i in isbn.isbnList:
    # regular expression. remove non-number.
    targetIsbn = re.sub(r'\D', "", i)
    if isIntType(targetIsbn):
        targetIsbn = int(targetIsbn)
        parser = SimpleParser(targetIsbn)
        if parser.data == '':
            continue
        else:
            data = Book(parser.data)
            database.append(data)
        time.sleep(3)

write.ExportResult(database)

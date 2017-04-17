# coding=UTF-8
from simpleparser import *
from bookcollection import *
import time

isbn = [9789862892077, 9789579556873 , 9789863360902, 9789888357802]

for i in isbn:
    parser = SimpleParser(i)
    data = BookCollection(parser.data)
    print(data.result)
    time.sleep(10)

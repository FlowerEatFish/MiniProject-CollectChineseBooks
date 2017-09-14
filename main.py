# coding=UTF-8
""" Python libraries. """
import time
import re
""" Libraries from here. """
import simpleparser
import book
import rwbook

ISBN = rwbook.Read()
DATABASE = []

for i in ISBN.isbn_list:
    target_isbn = re.sub(r'\D', "", str(i)) # regular expression. remove non-number.
    if bool(target_isbn) and target_isbn is not None:
        target_isbn = int(target_isbn)
        parser = simpleparser.SimpleParser(target_isbn)
        if parser.data == '':
            continue
        else:
            data = book.Book(parser.data)
            DATABASE.append(data)
        time.sleep(1)

rwbook.Write(DATABASE)

import json
from isbnlib import *
from BookClass import *
from json import *
from databaseClass import *
from flask import Flask, render_template, request, redirect, url_for
from sort import *
import routes
#-------VARS---------
ISBN = ["978-1-60309-388-0","9780452279605", "9780747532743", "978-1-60309-456-6", "978-1-60309-402-3", "978-1-60309-448-1", "9783863524586", "9781423121701"]
#--------------------

def testResetFunc():
    wipeDatabase()
    for isbn in ISBN:
        print("Trying " + isbn)
        try:
            book = Book.withIsbn(isbn, True, [])
            saveToDatabase(book)
        except:
            print("Book is unable to be saved via ISBN, please save it manually.")

if __name__ == '__main__':
    #testResetFunc()
    routes.app.run()


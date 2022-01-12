import json
from isbnlib import *
from BookClass import *
from ReviewClass import *
from json import *
from databaseClass import *
from flask import Flask, render_template, request, redirect, url_for

#-------VARS---------
ISBN = ["978-1-60309-388-0","9780452279605", "9780747532743", "978-1-60309-456-6", "978-1-60309-402-3", "978-1-60309-448-1", "9783863524586", "9781423121701"]
app = Flask(__name__)
#--------------------
wipeDatabase()
for isbn in ISBN:
    print("Trying " + isbn)
    try:
        book = Book.withIsbn(isbn, True, [])
        saveToDatabase(book)
    except:
        print("Book is unable to be saved via ISBN, please save it manually.")


"""for isbn in ISBN:
    try:
        print(meta(isbn, 'openl'))
    except:
        print(meta(isbn, 'goob'))


for isbn in ISBN:
    print("Trying " + isbn)
    try:
        book = Book.withIsbn(isbn, True, [])
        saveToDatabase(book)
    except:
        print("Book is unable to be saved via ISBN, please save it manually.")
#book = Book("The Dark Tower", "Stephen King", "June 10, 1982", False, ["Fantasy", "Horror"])
#book2 = Book("Winnie the pooh", "Christopher Robin", "April 10, 2006", True, ["Kids Book", "Fantasy"])
#book = Book.withIsbn("9780452279605", True, [])
#book2 = Book.withIsbn("9780747532743", True, [])
#saveToDatabase(book)
#saveToDatabase(book2)
#loaded_books = loadDatabase()

#for book in loaded_books:
#    print(book.bookName + " was written by " + book.author)



#9780452279605
"""


#-----------------Hey, we're actually programming!---------------------------------

@app.route('/')
def index():
    books = loadDatabase()
    return render_template('basic_table.html', title='Library',
                           books=books)
@app.route('/book/<bookName>')
def bookRoute(bookName):
        title = bookName
        database = loadDatabase()

        for book in database:
            if book.bookName == title:
                return render_template('book_display.html', book = book)
        return()

@app.route('/book/check_out/<bookName>', methods =["GET", "POST"])
def checkOut(bookName):
        title = bookName
        database = loadDatabase()
        if request.method == "POST":
            for book in database:
                if book.bookName == title:
                    checkedOutDate = request.form['submit_date']
                    studentName = request.form['student_name']
                    book.checkedIn = False
                    book.checkedOutBy = studentName
                    book.checkedOutDate = checkedOutDate
            print(type(database))
            overrideDatabase(database)
            return redirect(url_for('index'))
        else:

            for book in database:
                if book.bookName == title:
                    return render_template("book_check_out.html")

@app.route('/<test>')
def test(test):
    return test + " test route."

if __name__ == '__main__':
    app.run()
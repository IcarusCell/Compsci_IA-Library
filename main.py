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
tagList = ['fiction', 'nonfiction', 'fantasy', 'sci-fi', 'horror']
#--------------------
"""
wipeDatabase()
for isbn in ISBN:
    print("Trying " + isbn)
    try:
        book = Book.withIsbn(isbn, True, [])
        saveToDatabase(book)
    except:
        print("Book is unable to be saved via ISBN, please save it manually.")
"""

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
                    checkedOutDate = str(request.form['submit_date'])
                    studentName = str(request.form['student_name'])
                    book.checkedIn = False
                    book.checkedOutBy = str(studentName)
                    book.checkedOutDate = str(checkedOutDate)
            overrideDatabase(database)
            return redirect(url_for('index'))
        else:

            for book in database:
                if book.bookName == title:
                    return render_template("book_check_out.html")

@app.route('/book/check_in/<bookName>')
def checkIn(bookName):
        title = bookName
        database = loadDatabase()
        for book in database:
            if book.bookName == title:
                book.checkedIn = True
                book.checkedOutBy = ''
                book.checkedOutDate = ''
        overrideDatabase(database)
        return redirect(url_for('index'))
@app.route('/book/remove/<bookName>')
def removeBook(bookName):
    title = bookName
    database = loadDatabase()
    for book in database:
        if book.bookName == title:
            database.remove(book)
    overrideDatabase(database)
    return redirect(url_for('index'))

@app.route('/book/review/<bookName>', methods =["GET", "POST"])
def review(bookName):
        title = bookName
        database = loadDatabase()
        if request.method == "POST":
            for book in database:
                if book.bookName == title:
                    summary = str(request.form['review'])
                    #score = int(request.form['score'])
                    #review = Review(score, summary)

                    book.reviews.append(summary)#review)
            overrideDatabase(database)
            return redirect(url_for('index'))
        else:

            for book in database:
                if book.bookName == title:
                    return render_template("book_review.html")

@app.route('/new_book/<bookLanguage>', methods =["GET", "POST"])
def createNewBook(bookLanguage):
        database = loadDatabase()
        if(bookLanguage == "english"):
            if request.method == "POST":
                print(request.form['bookName'])
                bookName = request.form['bookName']
                print(request.form['authorName'])
                authorName = request.form['authorName'].split(",")
                print(authorName)
                print(request.form['datePublished'])
                datePublished = request.form['datePublished']
                print(request.form['onIbReadingList'])
                onIbReadingList = False
                if request.form['onIbReadingList'] == 'Yes':
                    onIbReadingList = True
                tags = []
                for tag in tagList:
                    try:
                        if request.form[tag] == 'True':
                            tags.append(tag)
                    except:
                        print('Tag is false')
                newBook = Book(bookName, authorName, datePublished, onIbReadingList, tags)
                database.append(newBook)
                overrideDatabase(database)
                return redirect(url_for('index'))
            else:
                return render_template("new_english_book.html", tags = tagList, bookLanguage = bookLanguage)
        elif(bookLanguage == "french"):
            return redirect(url_for('index'))
        else:
            print('Error')
            return redirect(url_for('index'))

@app.route('/new_book/<bookLanguage>/isbn', methods =["GET", "POST"])
def createNewBookISBN(bookLanguage):
        database = loadDatabase()
        if(bookLanguage == "english"):
            if request.method == "POST":
                isbnNum = request.form['isbnNum']
                onIbReadingList = False
                if request.form['onIbReadingList'] == 'Yes':
                    onIbReadingList = True
                tags = []
                for tag in tagList:
                    try:
                        if request.form[tag] == 'True':
                            tags.append(tag)
                    except:
                        print('Tag is false')
                newBook = Book.withIsbn(isbnNum, onIbReadingList, tags)
                database.append(newBook)
                overrideDatabase(database)
                return redirect(url_for('index'))
            else:
                return render_template("new_english_book_isbn.html", tags = tagList)
        elif(bookLanguage == "french"):
            return redirect(url_for('index'))
        else:
            print('Error')
            return redirect(url_for('index'))

@app.route('/book/edit/<bookTitle>/<bookLanguage>', methods =["GET", "POST"])
def editBook(bookTitle, bookLanguage):
        database = loadDatabase()
        if(bookLanguage == "english"):
            if request.method == "POST":
                for book in database:
                    if book.bookName == bookTitle:
                        if request.form['bookName'] != '':
                            bookName = request.form['bookName']
                        else:
                            bookName = book.bookName
                        if request.form['authorName'] != '':
                            authorName = request.form['authorName'].split(",")
                        else:
                            authorName = book.author
                        if request.form['datePublished'] != '':
                            datePublished = request.form['datePublished']
                        else:
                            datePublished = book.publishedDate
                        try:
                            print('Cleared IB Reading list check')
                            onIbReadingList = False
                            if request.form['onIbReadingList'] == 'Yes':
                                onIbReadingList = True
                        except:
                            onIbReadingList = book.onIbReadingList
                        tags = []
                        tagSelect = False
                        for tag in tagList:
                            try:
                                if request.form[tag] == 'True':
                                    tagSelect = True
                            except:
                                print('Tag check is false')
                        if tagSelect == True:
                            for tag in tagList:
                                try:
                                    if request.form[tag] == 'True':
                                        tags.append(tag)
                                except:
                                    print('Tag is false')
                        else:
                            tags = book.tags
                        check = 0
                        for title in database:
                            if title.bookName == book.bookName:
                                database.pop(check)
                            check += 1
                        newBook = Book(bookName, authorName, datePublished, onIbReadingList, tags)
                        database.append(newBook)
                        overrideDatabase(database)
                        print('Running through POST code')
                        return redirect(url_for('index'))
            else:
                print('Running through non-POST code')
                return render_template("edit_english_book.html", tags = tagList, bookLanguage = bookLanguage)
        elif(bookLanguage == "french"):
            return redirect(url_for('index'))
        else:
            print(bookLanguage)
            print('Error')
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
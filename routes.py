#--databaseClass.py is imported to allow the routes to interact with the database information--
#--flask is imported to allow the creation of routes as well as interaction with the HTML templates--
from databaseClass import *
from flask import Flask, render_template, request, redirect, url_for

#-------VARS---------

#--Declaring the web application run in main.py--
app = Flask(__name__)
#--The list of tags that can be used when creating or editing a book--
tagList = ['fiction', 'fantasy', 'sci-fi', 'horror', 'romance','crime', 'western', 'nonfiction', 'autobiography', 'biography', 'history', 'science', 'mathematics', 'biology', 'philosophy']

#--------------------

#--Home route, the place that a user first lands when entering the website
#The database is loaded and pased into the basic_table HTML template, displaying
#the library database.--
@app.route('/')
def index():
    books = loadDatabase()
    return render_template('basic_table.html', title='Library',
                           books=books)
#--Book display route, showcases the basic information about a title, dictated
#by book_display.html.--
@app.route('/book/<bookName>')
def bookRoute(bookName):
        title = bookName
        database = loadDatabase()

        for book in database:
            if book.bookName == title:
                return render_template('book_display.html', book = book)
        return()
#--Check out route, gets directed too from the book display route when a user
#indicates that a book is being checked out. If forum data has not been submitted
#this route loads the book_check_out html template, if data has been submitted
#it redirects to the home route.--
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

#--The opposite of the check out route, this is the check in route.
#It requires no data entry to it simply reverts all the check-out
#values to their default state and redirects to the root.--
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
#--The remove book route deletes all instances of a certain book
#title from the database and then redirects back to the root. This
#means that if there are duplicates of a certain book that have
#been created on accident, all will be deleted.--
@app.route('/book/remove/<bookName>')
def removeBook(bookName):
    title = bookName
    database = loadDatabase()
    for book in database:
        if book.bookName == title:
            database.remove(book)
    overrideDatabase(database)
    return redirect(url_for('index'))

#--The book review route directs to the book_review html template
#when the forum detects no data. When data is detected, the review
#is appended to the existing book object and the database is overriden--
@app.route('/book/review/<bookName>', methods =["GET", "POST"])
def review(bookName):
        title = bookName
        database = loadDatabase()
        if request.method == "POST":
            for book in database:
                if book.bookName == title:
                    summary = str(request.form['review'])
                    book.reviews.append(summary)
            overrideDatabase(database)
            return redirect(url_for('index'))
        else:

            for book in database:
                if book.bookName == title:
                    return render_template("book_review.html")

#--The book creation route. This route checks to see if the new_book
#html template forum has data present. If it does it redirects to the
#root. If not it loads the new_book template and allows the user to input
#the necessary information to generate a new book object.--
@app.route('/new_book/', methods =["GET", "POST"])
def createNewBook():
        database = loadDatabase()
        if request.method == "POST":
            if request.form['bookName'] == '':
                return redirect(url_for('index'))
            bookName = request.form['bookName']
            authorName = request.form['authorName'].split(",")
            datePublished = request.form['datePublished']
            onIbReadingList = False
            try:
                if request.form['onIbReadingList'] == 'Yes':
                    onIbReadingList = True
            except:
                print('No value for onIbReadingList')
            tags = []
            for tag in tagList:
                try:
                    if request.form[tag] == 'True':
                        tags.append(tag)
                except:
                    print('Tag is false')
            originalLanguage = str(request.form['originalLanguage'])
            newBook = Book(bookName, authorName, datePublished, onIbReadingList, tags)
            if originalLanguage != '':
                newBook.originalLanguage = originalLanguage
            else:
                newBook.originalLanguage = 'English'
            database.append(newBook)
            overrideDatabase(database)
            return redirect(url_for('index'))
        else:
            return render_template("new_english_book.html", tags = tagList)

#--This is the new book route that uses ISBN fetching, it is redirected
#too from the new book route. It uses similar logic but instead uses the
#Book.withIsbn function to generate the book object.--
@app.route('/new_book/isbn', methods =["GET", "POST"])
def createNewBookISBN():
        database = loadDatabase()
        if request.method == "POST":
            isbnNum = request.form['isbnNum']
            onIbReadingList = False
            try:
                if request.form['onIbReadingList'] == 'Yes':
                    onIbReadingList = True
            except:
                print('No value for onIbReadingList')
            tags = []
            for tag in tagList:
                try:
                    if request.form[tag] == 'True':
                        tags.append(tag)
                except:
                    print('Tag is false')
            newBook = Book.withIsbn(isbnNum, onIbReadingList, tags)
            if newBook is None:
                return redirect(url_for('index'))
            originalLanguage = str(request.form['originalLanguage'])
            newBook.originalLanguage = originalLanguage
            database.append(newBook)
            overrideDatabase(database)
            return redirect(url_for('index'))
        else:
            return render_template("new_english_book_isbn.html", tags = tagList)
#--This is the edit book route and is the longest in terms of length due to the
#significant amount of if/else statements needed to properly account for blank
#data entries. Essentially, any field that is left blank will not be overriden
#allowing the values present in the original book object that is now being edited
#to remain untouched, while the desired changes DO override the original book
#object's declared variables. Other than that is uses nearly identical logic
#to the new book route.--
@app.route('/book/edit/<bookTitle>/', methods =["GET", "POST"])
def editBook(bookTitle):
        database = loadDatabase()
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
                    bookBackup = ''
                    for title in database:
                        if title.bookName == book.bookName:
                            bookBackup = database[check]
                            database.pop(check)
                        check += 1
                    newBook = Book(bookName, authorName, datePublished, onIbReadingList, tags)
                    try:
                        newBook.checkedIn = bookBackup.checkedIn
                        newBook.checkedOutBy = bookBackup.checkedOutBy
                        newBook.checkedOutDate = bookBackup.checkedOutDate
                    except:
                        print('No book found')

                    database.append(newBook)
                    overrideDatabase(database)
                    return redirect(url_for('index'))
        else:
            return render_template("edit_english_book.html", tags = tagList)

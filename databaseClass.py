import json

from BookClass import *
import json
def saveToDatabase(book):
    with open('data\database.json', 'r+') as database:
        jsonFile = json.load(database)

        detailDict = {
                'Book Name':book.bookName,
                'Author': book.author,
                'ISBN Num': book.isbnNum,
                'Published Date': book.publishedDate,
                'On IB Reading List': book.onIbReadingList,
                'Checked In': book.checkedIn,
                'Tags': book.tags,
                'Reviews': book.reviews,
                'Checked out by:': book.checkedOutBy,
                'Checked out date': book.checkedOutDate
        }
        jsonFile["stored_books"].append(detailDict)
        database.seek(0)
        json.dump(jsonFile, database, indent=4)
        database.truncate()

#A function to completely empty the database (mainly used for testing)
def wipeDatabase():
    #Open the database file in the data directory
    with open('data\database.json', 'r+') as database:
        #The database is loaded into an array of dictionaries
        jsonFile = json.load(database)
        #The array is cleared of dictionaries
        jsonFile["stored_books"].clear()
        #The array is then saved to the database file
        database.seek(0)
        json.dump(jsonFile, database, indent=4)
        database.truncate()

#Function for loading the database into a list
def loadDatabase():
        #Instantiate a new list called books
        books = []
        #Open the database file in the data directory
        with open('data\database.json') as database:
            #The database is loaded into an array of dictionaries
            jsonFile = load(database)
            #For each book in the dictionary, it is saved to a book object using the information from the database.
            #The book is then appended to the books list.
            for book in jsonFile["stored_books"]:
               newBook = Book(book["Book Name"], book["Author"], book["Published Date"], book["On IB Reading List"], book["Tags"])
               newBook.checkedIn = bool(book["Checked In"])
               newBook.checkedOutBy = str(book["Checked out by:"])
               newBook.isbnNum = str(book["ISBN Num"])
               newBook.reviews = book["Reviews"]
               newBook.checkedOutDate = str(book['Checked out date'])
               books.append(newBook)
        return books

def overrideDatabase(newDatabase):
    wipeDatabase()
    for book in newDatabase:
        saveToDatabase(book)

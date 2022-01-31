#--the databaseClass.py script is imported to allow for managing of the database in the testResetFunc() script--
#--routes.py is imported so that the website can be ran--
from databaseClass import *
import routes
#-------VARS---------

#--List of active ISBN numbers for use with testResetFunc()--
ISBN = ["978-1-60309-388-0","9780452279605", "9780747532743", "978-1-60309-456-6", "978-1-60309-402-3", "978-1-60309-448-1", "9783863524586", "9781423121701"]
#--------------------
#--This function exists purely for testing purposes, but is being left in for future debugging if it becomes necessary. This function wipes the entire database and replaces
#it with a set of books fetched using ISBN numbers. Useful for testing alterations to the database and book creation functions.--
def testResetFunc():
    wipeDatabase()
    for isbn in ISBN:
        print("Trying " + isbn)
        try:
            book = Book.withIsbn(isbn, True, [])
            saveToDatabase(book)
        except:
            print("Book is unable to be saved via ISBN, please save it manually.")


#--Runs the web application created in the routes.py script--
if __name__ == '__main__':
    routes.app.run()


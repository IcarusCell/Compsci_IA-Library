#--isbnlib imported to allow support for ISBN based fetching functionality--
#--sort.py is imported for use with sorting names and tags in newly created book objects.--
from isbnlib import *
from sort import *
#--VARS--
    #Book Class:
        #String bookName
        #String[] tags
        #String isbnNum
        #String[] author
        #bool checkedIn
        #String publishedDate
        #String returnDate
        #String checkedOutDate
        #bool onIbReadingList
        #String[] reviews
        #String checkedOutBy
        #String authorString
        #String tagString
        #String originalLanguage
#--------

class Book:
    def __init__(self, bookName, author, publishedDate, onIbReadingList, tags):
        self.bookName = bookName
        #--Logic that checks for duplicate author names (done due to occasional strangeness with ISBN fetching), and then sorts them
        #alphabetically using the functions created in sort.py--
        cleanNames = []
        for name in author:
            if name not in cleanNames:
                cleanNames.append(name)
        self.author = sort(cleanNames)
        self.isbnNum = ''
        self.publishedDate = publishedDate
        self.onIbReadingList = onIbReadingList
        self.checkedIn = True
        #--Repeated logic from cleanNames--
        cleanTags = []
        for tag in tags:
            if tag not in cleanTags:
                cleanTags.append(tag.capitalize())
        self.tags = sort(cleanTags)
        self.reviews = []
        self.checkedOutBy = ''
        self.authorString = self.authorNamesInString()
        self.tagString = self.tagsInString()
        self.checkedOutDate = ''
        self.originalLanguage = 'English'
    #--A method that can be called to create a book object using an ISBN number as the primary source of data.--
    @classmethod
    def withIsbn(cls, isbnNum, onIbReadingList, tags):
        #--ISBN num is cast to a string so it can be parsed by isbnlib--
        isbnNum = str(isbnNum)
        isbnReal = isbnNum
        #--Checks if the ISBN number is real--
        if is_isbn13(isbnReal) or is_isbn10(isbnReal):
            #--Line of try/except logic checking various APIs for the ISBN number. If one fails it falls back to the others.--
            try:
                book = fillISBN(isbnReal, onIbReadingList, tags, 'openl')
            except:
                try:
                    book = fillISBN(isbnReal, onIbReadingList, tags, 'wiki')
                except:
                    book = fillISBN(isbnReal, onIbReadingList, tags, 'openl')
            #--Runs the isbnNum function declared below--
            book.isbnNum = isbnNum
            return book
        else:
            print('This is not a valid ISBN number')
        print("An error has occured, please input information manually.")

    #--Converts the array of author names passed in by an ISBN number or the basic constructor and converts it into a String--
    def authorNamesInString(self):
        authorString = self.author[0]
        if len(self.author) > 1:
            iter = 0
            while iter < (len(self.author)-1):
                iter += 1
                authorString = authorString + " and " + self.author[iter]

        return authorString

    # --Same as above, except for the tags--
    def tagsInString(self):
        if len(self.tags) > 0:
            tagString = self.tags[0]
            if len(self.tags) > 1:
                iter = 0
                while iter < (len(self.tags)-1):
                    iter += 1
                    tagString = tagString + ", " + self.tags[iter]
            print(tagString)
            return str(tagString)
        return
#--Generates a book object using information grabbed from an ISBN number--
def fillISBN(isbn, readingList, tags, key):
    isbnGrab = meta(isbn, key)
    print(isbnGrab)
    book = Book(isbnGrab['Title'], isbnGrab['Authors'], isbnGrab['Year'], readingList, tags)
    return book

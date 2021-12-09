from isbnlib import *
from json import *
#Book Class:
    #String[] tags
    #String isbnNum
    #String[] author
    #String bookName
    #bool checkedIn
    #String publishedDate
    #String returnDate
    #String checkedOutDate
    #bool onIbReadingList
    #Review[] reviews
    #String checkedOutBy
class Book:
    def __init__(self, bookName, author, publishedDate, onIbReadingList, tags):
        self.bookName = bookName
        cleanNames = []
        for name in author:
            if name not in cleanNames:
                cleanNames.append(name)
        self.author = cleanNames

        self.isbnNum = ''
        self.publishedDate = publishedDate
        self.onIbReadingList = onIbReadingList
        self.checkedIn = True
        cleanTags = []
        for tag in tags:
            if tag not in cleanTags:
                cleanTags.append(tag)
        self.tags = cleanTags
        self.reviews = []
        self.checkedOutBy = ""
        self.authorString = self.authorNamesInString()
        self.tagString = self.tagsInString()

    @classmethod
    def withIsbn(cls, isbnNum, onIbReadingList, tags):
        isbnNum = str(isbnNum)
        isbnReal = isbnNum
        if is_isbn13(isbnReal) or is_isbn10(isbnReal):
            print('Filling book object from ISBN num...')
            #print(desc(isbnReal))
            try:
                book = fillISBN(isbnReal, onIbReadingList, tags, 'openl')
            except:
                try:
                    print('Trying alternative API...')
                    book = fillISBN(isbnReal, onIbReadingList, tags, 'wiki')
                except:
                    book = fillISBN(isbnReal, onIbReadingList, tags, 'openl')
            #print(book)
            book.isbnNum = isbnNum
            return book
        else:
            print('This is not a valid ISBN number')
        print("An error has occured, please input information manually.")


    def authorNamesInString(self):
        authorString = self.author[0]
        if len(self.author) > 1:
            iter = 0
            while iter < (len(self.author)-1):
                iter += 1
                authorString = authorString + " and " + self.author[iter]

        return authorString

    def tagsInString(self):
        if len(self.tags) > 0:
            tagString = self.tags[0]
            if len(self.tags) > 1:
                iter = 0
                while iter < (len(self.tags)-1):
                    iter += 1
                    authorString = tagString + "," + self.author[iter]

            return tagString
        return



def fillISBN(isbn, readingList, tags, key):
    isbnGrab = meta(isbn, key)
    print(isbnGrab)
    book = Book(isbnGrab['Title'], isbnGrab['Authors'], isbnGrab['Year'], readingList, tags)
    return book
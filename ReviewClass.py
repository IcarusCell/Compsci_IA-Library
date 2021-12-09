#Review Object:
    #double rating
        #Stores the rating out of 5 that the user gave to the book.
    #String review
        #A text review of the book, could be excluded at user discretion.
class Review:
    def __init__(self, rating, review):
        self.rating = rating
        self.review = review
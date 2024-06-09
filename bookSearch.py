#File no:   2
#filename : bookSearch.py
#Date 5/12/2022
#By F213619
"""
This module contains the core functions for the book search system.
"""


##########################################################
##                        MAIN                          ##
##########################################################

import database

def search(name:str):
    """
    This function searches the bookinfo.txt file for a book based on its title and returns
    a complete list of books with all their associated information 
    (e.g., title, author, genre and loan availability, etc.)
    The format of the output will be : [[BookID,GenreName,BookName,AuthorName,Price,PurchaseDate]]
    """
    library = database.getBooks()
    isfound = False
    rightbook = []
    for book in library:
        info = book.split(',')
        if name == info[2]:
            rightbook += [info]
            isfound = True
    if isfound == False:
        return "We do not have this book"
    return rightbook
    

if __name__ == "__main__":
    #testing the search function :
    print(search("PlanetOfTheApes")) #in database : one occurence
        #prints : [['0002', 'Sci-Fi', 'PlanetOfTheApes', 'PierreBoulle', '10', '2010-8-1']]
    print(search("ThePhilosophersStone")) #in database : multiple occurences - prints 
        #prints : [['0006', 'Fantasy', 'ThePhilosophersStone', 'JKRowling', '10', '2004-6-8'], ['0010', 'Fantasy', 'ThePhilosophersStone', 'JKRowling', '10', '2013-12-12']]
    print(search("TheHitchikersGuideToTheGalaxy")) #not in database
        #prints : We do not have this book

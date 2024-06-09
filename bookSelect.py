#File no:   5
#filename : bookSelect.py
#Date 5/12/2022
#By F213619
"""
This module contains the core functions for the select system.
"""

import database
import matplotlib.pyplot as plt


####################### search-related functions #######################

def sortByPopularity_Books():
    """
    This function searches through the logfile.txt file and counts the number of times each book was taken out
    with the use of a dictionary, then sorts the elements into a list by descending order.
    The output will be a list of tuples of the form : [(BookID,nb_logs)] with (BookID : Str) and (nb_logs : Int)
    """
    database.getLogs()
    library = {}
    for entry in database.Logs :
        if entry[0] not in library.keys():
            library[entry[0]] = 1
        else:
            library[entry[0]] += 1
    database.clearLogs()
    sorted_library_items = sorted(library.items(), key = lambda x : x[1], reverse = True)
    return sorted_library_items


def sortByPopularity_Genre():
    """
    This function searches through the logfile.txt and bookinfo.txt files, counting the number of times a book of a
    particular genre was taken out with the use of a dictionary, then sorts the elements into a list by descending order.
    The output will be a list of tuples of the form : [(GenreName,nb_logs)] with (GenreName : Str) and (nb_logs : Int)
    """
    database.getLogs()
    library = database.getBooks()
    mostPopGenre = {}
    for entry in database.Logs :
        for book in library :
            info = book.split(',')
            if entry[0] != info[0] :
                #checks if the bookID's match : if not then goes to following book in library
                pass
            else :
                #if the bookID's match : we add the book's genre to the dictionary
                if info[1] not in mostPopGenre.keys():
                    #situation where the genre hasn't already been added to the dictionary : initialise the value
                    mostPopGenre[info[1]] = 1
                else :
                    #situation where the genre has already been added to the dictionary : increment value
                    mostPopGenre[info[1]] += 1
    database.clearLogs()
    sorted_genre_items = sorted(mostPopGenre.items(), key = lambda x : x[1], reverse = True)
    return sorted_genre_items

def sortByPrice_Genre():
    """
    This function searches through the bookinfo.txt file, sorting each genre from most expensive to least
    (we presume that each genre has a set price, in order to facilitate the sorting process)
    The output will be a list of tuples of the form : [(GenreName,Genre_prirce)] with (GenreName : Str) and (Genre_price : Int)
    """
    library = database.getBooks()
    GenrePrices = {}
    for book in library :
        info = book.split(',')
        if info[1] not in GenrePrices.keys():
            #situation where the genre hasn't already been added to the dictionary : initialise the value
            GenrePrices[info[1]] = int(info[4])
        else :
            pass
    
    sortedByPrice_genre_items = sorted(GenrePrices.items(), key = lambda x : x[1], reverse = True)
    return sortedByPrice_genre_items


def mostPopularBook():
    """
    This function uses the sortByPopularity_Books function to return the BookID of the most popular book
    The output will be a string of the form : "0000"
    """
    sorted_library_items = sortByPopularity_Books()
    sorted_library_books = [x for (x,y) in sorted_library_items]
    return sorted_library_books[0]


def mostPopularGenre():
    """
    This function uses the sortByPopularity_Genre function to return the GenreName of the most popular genre
    The output will be a string of the form : "Fantasy"
    """
    sorted_genre_items = sortByPopularity_Genre()
    sorted_genres = [x for (x,y) in sorted_genre_items]
    return sorted_genres[0]


def findBookPrice(genre):
    """
    This function takes as a parameter a String corresponding to a book's genre, and returns the corresponding price.
    We assume that all books of a particular genre cost the same.
    The output will be an integer
    """
    library = database.getBooks()
    for book in library:
        info = book.split(',')
        if genre != info[1]:
            pass 
        else :
            return int(info[4])
        

def budgetReccomendation(budget):
    """
    This function splits the overall budget into sections, assigning sub-budgets to each genre based on their popularity 
    (we wish to invest more in the genres which are most popular).
    This function takes as a parameter an integer and returns a list comprised of tuples of the form (genre_name,genre_budget)
    """
    genre_popularity = sortByPopularity_Genre()
    total_nb = database.totalNbEntries()
    SplitBudget = []
    for genre in genre_popularity :
        genre_name = genre[0]
        proportion = genre[1] / total_nb
        genre_budget = proportion * budget
        SplitBudget += [(genre_name,genre_budget)]
    return SplitBudget


def reccomendationList(budget):
    """
    This function takes as a parameter an integer corresponding to the budget for a book purchase, and returns a list comprised of tuples
    corresponding to each genre and the respective number of books to purchase and the leftover change from the purchase.
    (We omit purchasing a fraction of a book, therefore we include a change variable)
    """
    budgets = budgetReccomendation(budget)
    nb_books = []
    change=0
    for tuple in budgets:
        genre = tuple[0]
        budget = tuple[1]
        price = findBookPrice(genre)
        nb_copies = budget // price

        change += budget - nb_copies*price
        nb_books += [(genre,nb_copies)]
    return nb_books, change


def suggestion(budget):
    """
    For the leftover budget, we inform the user what they can still purchase.
    """
    sorted_Genres = sortByPrice_Genre()
    nb_books = []
    for tuple in sorted_Genres :
        genre = tuple[0]
        price = tuple[1]
        nb_copies = budget // price
        nb_books += [(genre,nb_copies)]
    return nb_books



        
            


####################### Matplotlib-related functions #######################

def showBookPopularity():   
    sorted_library_items = sortByPopularity_Books()
    sorted_library_books = [x for (x,y) in sorted_library_items]
    sorted_library_values = [y for (x,y) in sorted_library_items]
    return sorted_library_books, sorted_library_values
    #plt.bar(sorted_library_books,sorted_library_values,color='blue')
    #plt.title("Book popularity")
    #plt.show()

def showGenrePopularity():
    sorted_genre_items = sortByPopularity_Genre()
    sorted_genres = [x for (x,y) in sorted_genre_items]
    sorted_genre_values = [y for (x,y) in sorted_genre_items]
    return sorted_genres,sorted_genre_values
    #plt.bar(sorted_genres,sorted_genre_values,color='blue')
    #plt.title("Genre popularity")
    #plt.show()


####################### Testing #######################

if __name__ == "__main__":
    print(sortByPopularity_Books()) 
    print(sortByPopularity_Genre())
    print(mostPopularBook())
    print(mostPopularGenre())
    print(findBookPrice("Gothic"))

##    print(showBookPopularity())
##    showGenrePopularity()
    print(budgetReccomendation(100))
    print(reccomendationList(100))
    print(sortByPrice_Genre())
    print(suggestion(50))

#File no:   4
#filename : bookReturn.py
#Date 5/12/2022
#By F213619
"""
This module contains the core function(s) for the return system.
"""

##########################################################
##                        MAIN                          ##
##########################################################

import database

def returnBook(Member_ID, Book_ID):
    """
    docstring
    """
    database.getLogs()
    Found = False
    for entry in database.Logs[::-1]:
        if entry[0] == Book_ID and entry[1] == Member_ID and entry[3] == "none": 
            #situation where the Book is found in the database and was checked out by user
            Found = True
            Return_Date = database.todays_date()
            entry[3] = Return_Date
            message = "You had indeed checked this book out.\nWe have returned it for you.\n"
            break
        elif entry[0] == Book_ID and entry[1] != Member_ID:
            #situation where the Book is found in the database but was not checked out by the user
            message = "Error : it does not appear as if you have checked this book out.\n"
            break
        else : 
            pass
    if Found == False:
        message = "Are you sure the book ID you have entered is valid?\nYou may already have returned the book.\n"
    database.writeAllLogs()
    database.clearLogs()
    return message



#If the ID is invalid, or the book is already available, the program should return an error message. 
# Otherwise, the database should be updated accordingly. Additionally, an appropriate message should 
# be displayed if the book is reserved by a member.


if __name__ == "__main__":
    print(returnBook("0000","0003")) #returns the book "0003" that we checked out in bookCheckout.py
    print(returnBook("0001","0003")) #returns an error message : "Error : it does not appear as if you have checked this book out"
#File no:   3
#filename : bookCheckout.py
#Date 5/12/2022
#By F213619
"""
This module contains the core functions for the checkout system.
"""

import database


##########################################################
##                        MAIN                          ##
##########################################################

def checkout(Member_ID, Book_ID):
    """
    appends checkout log into logfile.txt (without return date)
    ! if book has multiple reservations then stays reserved

    """
    database.clearLogs()
    database.getLogs()
    Found = False
    for entry in database.Logs[::-1]: #search through the logfile backwards in order to find the most recent entry
        if entry[0] == Book_ID:
            Found = True
            if entry[3] == "none": 
                #situation where the Book is found in the database but it is unavailable (no return date)
                database.reserve(entry,Member_ID)
                message = "This book is currently unavailable.\nWe have reserved it for you.\n"

            else:
                #situation where the Book is found and available (there is a return date)
                Checkout_Date = database.todays_date()
                if entry[4] == "available":
                    #the book is available and has no reservations
                    database.writeLog(Book_ID,Member_ID,Checkout_Date,"none","available")
                    message = "The book is available.\nWe have checked it out for you.\n"                

                if Member_ID == database.nextReserve(entry):
                    #the book is available and you are at the head of the reservation queue
                    reservations = database.getReservationList(entry)
                    database.writeLog(Book_ID,Member_ID,Checkout_Date,"none",reservations)
                    message = "We see you have already reserved this book.\nIt is now available and we have checked it out for you.\n"

                else:
                    #the situation where book is available but it has been reserved
                    database.reserve(entry,Member_ID)
                    message = "This book is currently unavailable.\nWe have reserved it for you.\n"
            break
        else:
            pass
    if Found == False:
        message = "We were unable to find this book's ID in the database"
    
    database.writeAllLogs() #applies all changes to the logfile.txt
    database.clearLogs() #resets Logs list for next instance of checkout
    return message


if __name__ == "__main__":
    print(checkout("0000","0003")) #should checkout book "0003"
    print(checkout("0001","0003")) #should reserve book "0003" under "0001"
    print(checkout("0002","0003")) #adds member "0002" to reservation list for book "0003"
    #we should have a new entry : 0003,0000,2022-12-11,none,0001-0002
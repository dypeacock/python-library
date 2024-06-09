#File no:   6
#filename : database.py
#Date 5/12/2022
#By F213619
"""
This module contains the core functions used to manipulate the database.

"""

import datetime 

####################### Bookinfo-related functions #######################

def getBooks():
    """
    This function has no parameters and returns an array of books under the format:
    [BookID,BookGenre,BookName,BookAuthor,PurchasePrice,PurchaseDate] where 
        BookID = a book's unique ID (str), e.g. 0016
        BookGenre = the genre to which the book belongs (str), e.g. fantasy
        BookName = the book's (non-unique) title (str), e.g. TheMartian
        BookAuthor = the Name and Surname of the book's author (str), e.g. AndyWeir
        PurchasePrice = the price at which the book is sold (int), e.g. 10
        PurchaseDate = the date at which the library purchased the book (str), e.g. 2022-11-24
    """
    f = open('bookinfo.txt',"r")
    list_books = []
    for line in f:
        n = line.strip()
        list_books.append(n)
    f.close()
    return list_books


def findBookName(BookID):
    """
    this function finds the Book's Name from a given bookID
    """
    library = getBooks()
    for book in library :
        info = book.split(',')
        if info[0] == BookID:
            return info[2]
        else :
            pass


####################### Logfile-related functions #######################

Logs = []

def add_log(Book_ID,Member_ID,Checkout_Date,Return_Date,Reserved):
    """
    Adds log [Book_ID,Member_ID,Checkout_Date,Return_Date,Reserved] to Logs (list)
        Book_ID = a book's unique ID (str), e.g. 0016
        Member_ID = a member's unique ID (str), e.g. 0108
        Checkout_Date = date of last checkout (str), e.g. 2017-6-12
        Return_Date = date of last return (str) - or if still on loan value = none
        Reserved = reservation status of the book (str), e.g. 0018-0067
    e.g. if Logs is [[0017,0000,"21/11/2018","3/12/2018","available"]] then calling
    add_log(0008,0000,"2020-4-21","2020-6-8","0018-0067") changes it to
    [["0017","0000","2018-11-21","2018-12-3","available"],[0008,0000,"2020-4-21","2020-6-8","0018-0067"]]
    """
    global Logs
    Logs.append([Book_ID,Member_ID,Checkout_Date,Return_Date,Reserved])

def getLogs():
    '''
        Opens a file in which a line is formatted as:
            Book_ID,Member_ID,Checkout_Date,Return_Date,Reserved
        e.g.
            0007,0000,2021-3-20,2021-12-9,available
        Eah line is read and the data added to the Logs list.
        Finally the file is closed.
        Parameters:
            none.
    '''
    f = open('logfile.txt',"r")
    for line in f:
        l = line.strip().split(',')
        Book_ID = l[0]
        Member_ID = l[1]
        Checkout_Date = l[2]
        Return_Date = l[3]
        Reserved = l[4]
        add_log(Book_ID,Member_ID,Checkout_Date,Return_Date,Reserved)
    f.close()

def writeLog(Book_ID:str,Member_ID:str,Checkout_Date:str,Return_Date:str,Reserved:bool):
    '''
        Adds an entry to the Logs list, and then writes out all the
        data contained in Logs to the logfile.txt in the format:
            Book_ID,Member_ID,Checkout_Date,Return_Date,Reserved
        e.g.
            0011,0000,2019-3-9,2020-4-21,False
            0008,0000,2020-4-21,2020-6-8,False
        Parameters:
            Book_ID = a book's unique ID (str), e.g. 0016
            Member_ID = a member's unique ID (str), e.g. 0108
            Checkout_Date = date of last checkout (str), e.g. 2017-6-12
            Return_Date = date of last return (str) - or if still on loan value = none
            Reserved = reservation status of the book (str), e.g. available OR 0000-0021-0004
    '''
    #assume Logs has already been initialised
    add_log(Book_ID,Member_ID,Checkout_Date,Return_Date,Reserved)
    writeAllLogs()


def writeAllLogs():
    """
    Overwrites any data contained in logfile.txt and replaces it with the 
    list of entries contained in Logs, line by line.
    """
    global Logs
    f = open('logfile.txt',"w")
    for line in Logs:
        f.write(f"{line[0]},{line[1]},{line[2]},{line[3]},{line[4]}\n")
    f.close()


def clearLogs():
    global Logs
    Logs = []


def totalNbEntries():
    getLogs()
    nb = len(Logs)
    clearLogs()
    return nb


def todays_date():
    date = str(datetime.date.today())
    return date


####################### Reservation-related functions #######################

def reserve(entry,Member_ID):
    if entry[4] == "available":
        entry[4] = Member_ID
    else :
        reservations = entry[4].split('-')
        reservations.append(Member_ID)
        entry[4] = "-".join(reservations)


def isReserved(entry):
    if entry[4] == "available":
        return False
    else:
        return True


def nextReserve(entry):
    reservations = entry[4].split('-')
    r = reservations.pop(0)
    return r


def getReservationList(entry):
    reservations = entry[4].split('-')
    r = reservations.pop(0)
    if reservations == [] :
        entry[4] = "available"
    else:
        entry[4] = "-".join(reservations)
    return entry[4]


####################### Member-related functions #######################

member_log = ["0000"] #ID nb 0000 : admin

def is_member(id):
    if id in member_log:
        return True
    else:
        if is_correct(id):
            c = str(input("We do not recognise this ID, do you wish to create a new MemberId?\
                \nType 'y' to continue, or type 'q' to quit\n"))
            if c == 'y':
                new_member()
            elif c == 'q':
                print("Thank You")
            else:
                print("Really?")
        else:
            print("ERROR : Invalid ID (must be a 4-digit integer)")
        

def is_correct(id:str):
    correct_char = "0123456789"
    for char in id:
        if char not in correct_char:
            return False
    return True

def new_member():
    newId = int(member_log[-1])+1 #need to have format XXXX
    if newId < 10:
        newId = "000"+str(newId)
    elif newId < 100:
        newId = "00"+str(newId)
    elif newId < 1000:
        newId = "0"+str(newId)
    else:
        pass
    #member_log.append(str(newId))
    print("your new MemberId is : %4s"%(newId))


####################### Testing #######################

if __name__ == "__main__":
    print("Bookinfo-related functions")
    print(getBooks()) # prints out a the complete list of books in the database
    print(findBookName("0001")) # should print the name of the book with ID : 0001 (TheMartian)
    print("")

    print("Logfile-related functions")
    add_log("0021","0000","2022-12-11","none","available")
    print(Logs) # prints the list containing the log ["0021","0000","2022-12-11","none","available"]
    clearLogs() # reinitialise Logs array : empties the Logs array
    print("")

    getLogs() # imports the log data from logfile.txt and appends it to the Logs array
    print(Logs) # should print the complete list of all logs in logfile.txt
    clearLogs() # reinitialise Logs array : empties the Logs array
    print("")
    
##    writeLog("0020","0000","2022-12-11","none","available") # adds the log to the Logs array and writes the data in logfile
##    print(Logs) # should only show [['0020', '0000', '2022-12-11', 'none', 'available']] as Logs array was empty beforehand
##    clearLogs() # reinitialise Logs array : empties the Logs array
##    print(totalNbEntries()) # should now show 1 as the data in logfile was overwritten
    print(todays_date()) # should print today's date
    print("")

    print("Reservation-related functions")
    entry = ["0020","0000","2022-12-11","none","available"]
    reserve(entry,"0001")
    print(entry) # should show the updated log : ['0020', '0000', '2022-12-11', 'none', '0001']
    print(isReserved(entry)) # should show the boolean value True
    print(nextReserve(entry)) # should show the next person in the reservation queue : 0001
    print(getReservationList(entry)) # should show the book's reservation list after being checked out by the next person in reservation queue : available
    print("")

    print("Member-related functions")
    print(is_correct("abcd")) # should return the boolean value False
    print(is_correct("0000")) # should return the boolean value True

#File no:   1
#filename : menu.py
#Date 5/12/2022
#By F213619
"""
This is the main module.
it shows the menu and expects user interaction.
"""

from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import database
import bookCheckout
import bookReturn
import bookSearch
import bookSelect

## All functions relating to displaying frames : 

def Checkout():
    """
    This function clears all frames other than the menu and the quit frame, then displays the checkout and output frame
    """
    clearReturnFrame()
    clearSearchFrame()
    clearSelectFrame()
    checkoutframe.grid(row=1,column=0,columnspan=2,rowspan=2)
    outputframe.grid(row=1,column=2,columnspan=2,rowspan=2)


def Return():
    """
    This function clears all frames other than the menu and the quit frame, then displays the return and output frame
    """
    clearCheckoutFrame()
    clearSearchFrame()
    clearSelectFrame()
    returnframe.grid(row=1,column=0,columnspan=2,rowspan=2)
    outputframe.grid(row=1,column=2,columnspan=2,rowspan=2)


def Search():
    """
    This function clears all frames other than the menu and the quit frame, then displays the search and output frame
    """
    clearCheckoutFrame()
    clearReturnFrame()
    clearSelectFrame()
    searchframe.grid(row=1,column=0,columnspan=2,rowspan=2)
    outputframe.grid(row=1,column=2,columnspan=2,rowspan=2)


def Select():
    """
    This function clears all frames other than the menu and the quit frame, then displays the select and output frame
    """
    clearCheckoutFrame()
    clearReturnFrame()
    clearSearchFrame()
    selectframe.grid(row=1,column=0,columnspan=2,rowspan=2)
    outputframe.grid(row=1,column=2,columnspan=2,rowspan=2)


def showCanvas():
    """
    This function displays the canvas frame
    """
    canvasframe.grid(column=0,row=3,columnspan=4)

## All functions related to clearing frames : 

def Quit():
    """
    This function destroys the TKinter window which contains all frames
    """
    window.quit()
    window.destroy()

def clearCheckoutFrame():
    """
    This function 'clears' the checkout and output frames by forgetting their grid positioning
    """
    checkoutframe.grid_forget()
    outputframe.grid_forget()

def clearReturnFrame():
    """
    This function 'clears' the return and output frames by forgetting their grid positioning
    """
    returnframe.grid_forget()
    outputframe.grid_forget()

def clearSearchFrame():
    """
    This function 'clears' the Search and output frames by forgetting their grid positioning
    """
    searchframe.grid_forget()
    outputframe.grid_forget()

def clearSelectFrame():
    """
    This function 'clears' the Select, output and canvas frames by forgetting their grid positioning
    """
    selectframe.grid_forget()
    outputframe.grid_forget()
    canvasframe.grid_forget()


## window and frame definitions

window = Tk()
window.wm_title("Library System")

mainmenu = Frame(window)
mainmenu.grid(column=0,row=0,columnspan=4)

quitbuttonframe = Frame(window)
quitbuttonframe.grid(column=0,row=4,columnspan=4)

checkoutframe = Frame(window)

returnframe = Frame(window)

searchframe = Frame(window)

selectframe = Frame(window)

outputframe = Frame(window)

canvasframe = Frame(window)


## content in menu frame :


checkout_button = Button(mainmenu, text="Checkout a book", command=Checkout)
checkout_button.grid(row=0, column=0,sticky='ew')

return_button = Button(mainmenu, text="Return a book", command=Return)
return_button.grid(row=0, column=1,sticky='ew')

search_button = Button(mainmenu, text="Search for a book", command=Search)
search_button.grid(row=0, column=2,sticky='ew')

select_button = Button(mainmenu, text="Select a book", command=Select)
select_button.grid(row=0, column=3,sticky='ew')


## content in quitbutton frame :


quit_button = Button(quitbuttonframe, text="Quit", command=Quit)
quit_button.grid(row=0, column=0,sticky='ew')


## content in output frame :


def cleartextbox():
    outputtext.delete(1.0, 'end')


outputtext = Text(outputframe,height=13,width=42,wrap=WORD)
outputtext.grid(row=1,column=0,pady=25)

clear_btn = Button(outputframe,text="clear",command=cleartextbox)
clear_btn.grid(row=2,column=0)


# checkout SubmitEntries function :

def SubmitEntries_Checkout():
    """
    This function checks that the input is valid and returns an error message if it's not,
    then displays an appropriate message and book reservation option if the book is not available due to the book being on loan.
    If the book is available, the librarian can withdraw the book and the related records in the database are updated accordingly.
    """
    Member_ID = ID_Entry.get()
    Book_ID = Book_Entry.get()
    if database.is_correct(Member_ID):
        message = bookCheckout.checkout(Member_ID,Book_ID)+"\n"
        outputtext.insert('end',message)  
    else :
        outputtext.insert('end',"The MemberID you have entered is invalid : please try again")

# return SubmitEntries function :

def SubmitEntries_Return():
    """
    If the ID is invalid, or the book is already available, this function displays an error message. 
    Otherwise, the database should be updated accordingly. 
    Additionally, an appropriate message is be displayed if the book is reserved by a member.
    """
    Member_ID = ID_Entry_2.get()
    Book_ID = Book_Entry_2.get()
    if database.is_correct(Member_ID):
        message = bookReturn.returnBook(Member_ID,Book_ID)+"\n"
        outputtext.insert('end',message)
    else :
        outputtext.insert('end',"The MemberID you have entered is invalid : please try again")

# search SubmitEntry function :

def SubmitEntry_Search():
    """
    This function enables the user to search for a book given its title.
    It displays a complete list of books with all their associated information.
    """
    output = Book_Entry_3.get()
    searchresult = bookSearch.search(output)
    if searchresult == "We do not have this book" :
        outputtext.insert('end',searchresult+f" : {output}")
    else :
        for book in searchresult :
            outputtext.insert('end',"========================\n")
            BookID = f"BookID : {book[0]}\n"
            Genre = f"Genre : {book[1]}\n"
            Name = f"Name : {book[2]}\n"
            Author = f"Author : {book[3]}\n"
            Price = f"Price : {book[4]}\n"
            Purchase_date = f"Purchase Date : {book[5]}\n"
            outputtext.insert('end',BookID+Genre+Name+Author+Price+Purchase_date)
            outputtext.insert('end',"========================\n")

# select SubmitEntry function :

def SubmitEntry_Select():
    """
    This function reccomends a number of books to purchase for each genre given a total budget.
    It also displays the leftover change after the reccomended purchase and a suggestion as to how best to invest it.
    """
    try :
        Budget = Select_Entry.get()
        selection, change = bookSelect.reccomendationList(int(Budget))
        outputtext.insert('end',f"For a budget of £{Budget}, it is reccomended that you purchase :\n\n")
        for tuple in selection :
            genre = tuple[0]
            quantity = tuple[1]
            outputtext.insert('end',f"{genre} - {quantity} books\n")
        outputtext.insert('end',"\nYou will be left with £%d\n\n"%(change))
        
        outputtext.insert('end',"With %d, you can for instance purchase :\n"%(change))
        suggestion = bookSelect.suggestion(change)
        for tuple in suggestion:
            genre = tuple[0]
            quantity = tuple[1]
            outputtext.insert('end',f"{genre} - {quantity} books\n")
        outputtext.insert('end',"Please note that you will not be able to purchase all of the above (EITHER/OR)\n")
    except ValueError:
        outputtext.insert('end',"Error : please enter an integer\n")

# select MostPopBook function :

def Most_Pop_Book():
    """
    This function displays the most popular book.
    """
    bookID = bookSelect.mostPopularBook()
    bookName = database.findBookName(bookID)
    message = f"The most popular book is :\nBook Name - {bookName}\nBookID - {bookID}\n"
    outputtext.insert('end',message) 

# select MostPopGenre function :

def Most_Pop_Genre():
    """
    This function displays the most popular genre.
    """
    genreName = bookSelect.mostPopularGenre()
    message = f"The most popular genre is :\n{genreName}\n"
    outputtext.insert('end',message) 

# select BookStatistics function :

def BookStatistics():
    """
    This function displays the graph containing statistics relating to book popularity

    """
    showCanvas()
    canvas1.draw()
    canvas1.get_tk_widget().grid(column=0,row=0)
    clearcanvas1_button.grid(column=0,row=1,sticky='ew')

# select GenreStatistics function :

def GenreStatistics():
    """
    This function displays the graph containing statistics relating to genre popularity
    """
    showCanvas()
    canvas2.draw()
    canvas2.get_tk_widget().grid(column=0,row=0)
    clearcanvas2_button.grid(column=0,row=1,sticky='ew')


## content in checkout frame : 


chechout_title = Label(checkoutframe, text="Checkout Menu :")
chechout_title.grid(row=0, column=0,columnspan=2)

ID_Entry = Entry(checkoutframe)
ID_Entry.grid(row=1, column=1,sticky='ew')

ID_label = Label(checkoutframe, text="Enter your member ID :")
ID_label.grid(row=1, column=0,sticky='ew')

Book_Entry = Entry(checkoutframe)
Book_Entry.grid(row=2, column=1,sticky='ew')

BookID_label = Label(checkoutframe, text="Enter the book ID :")
BookID_label.grid(row=2, column=0,sticky='ew')

Submit = Button(checkoutframe, text="Submit", command=SubmitEntries_Checkout)
Submit.grid(row=3, column=0,columnspan=2,sticky='ew')

Exit = Button(checkoutframe, text="exit",command=clearCheckoutFrame)
Exit.grid(row=4, column=0,columnspan=2,sticky='ew')


## content in return frame :


return_title = Label(returnframe, text="Return Menu :")
return_title.grid(row=0, column=0,columnspan=2)

ID_Entry_2 = Entry(returnframe)
ID_Entry_2.grid(row=1, column=1,sticky='ew')

ID_label_2 = Label(returnframe, text="Enter your member ID :")
ID_label_2.grid(row=1, column=0,sticky='ew')

Book_Entry_2 = Entry(returnframe)
Book_Entry_2.grid(row=2, column=1,sticky='ew')

BookID_label_2 = Label(returnframe, text="Enter the book ID :")
BookID_label_2.grid(row=2, column=0,sticky='ew')

Submit_2 = Button(returnframe, text="Submit", command=SubmitEntries_Return)
Submit_2.grid(row=3, column=0,columnspan=2,sticky='ew')

Exit_2 = Button(returnframe, text="exit",command=clearReturnFrame)
Exit_2.grid(row=4, column=0,columnspan=2,sticky='ew')


## content in search frame :


search_title = Label(searchframe, text="Search Menu :")
search_title.grid(row=0,column=0)

Book_Entry_3 = Entry(searchframe)
Book_Entry_3.grid(row=1, column=0,sticky='ew')

Submit_3 = Button(searchframe, text="Submit", command=SubmitEntry_Search)
Submit_3.grid(row=2, column=0,sticky='ew')

Exit_3 = Button(searchframe, text="exit",command=clearSearchFrame)
Exit_3.grid(row=3, column=0,sticky='ew')


## content in select frame :

select_title = Label(selectframe, text="Select Menu :")
select_title.grid(row=0,column=0,columnspan=2)

MostPopBook = Button(selectframe, text="Most Popular Book", command=Most_Pop_Book)
MostPopBook.grid(row=1, column=0,columnspan=2,sticky='ew')

MostPopGenre = Button(selectframe, text="Most Popular Genre", command=Most_Pop_Genre)
MostPopGenre.grid(row=2, column=0,columnspan=2,sticky='ew')

BookStats = Button(selectframe,text="See Book Statistics",command=BookStatistics)
BookStats.grid(row=3,column=0,columnspan=2,sticky='ew')

GenreStats = Button(selectframe,text="See Genre Statistics",command=GenreStatistics)
GenreStats.grid(row=4,column=0,columnspan=2,sticky='ew')

Select_label = Label(selectframe,text="Enter the budget for the search :")
Select_label.grid(row=5,column=0,sticky='ew')

Select_Entry = Entry(selectframe)
Select_Entry.grid(row=5,column=1,sticky='ew')

Select_submit = Button(selectframe,text="Submit",command=SubmitEntry_Select)
Select_submit.grid(row=6,column=0,columnspan=2,sticky='ew')

Exit_4 = Button(selectframe,text="exit",command=clearSelectFrame)
Exit_4.grid(row=7,column=0,columnspan=2,sticky='ew')


## content in canvas frame :


sorted_library_books,sorted_library_values = bookSelect.showBookPopularity()
sorted_genres,sorted_genre_values = bookSelect.showGenrePopularity()

def bookgraph(sorted_library_books,sorted_library_values):
    """
    This function creates a new graph containing the popularity data of each book
    """
    fig = plt.figure(figsize=(5,2))
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(sorted_library_books,sorted_library_values,'r-')
    #fig = plt.bar(sorted_library_books,sorted_library_values,color='blue')
    return fig

def genregraph(sorted_genres,sorted_genre_values):
    """
    This function creates a new graph containing the popularity data of each genre
    """
    fig = plt.figure(figsize=(5,2))
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(sorted_genres,sorted_genre_values,'r-')
    return fig

def clearcanvas1():
    """
    This function clears the data in canvas1 (contains the bookfigure graph)
    ! Problem : deletes every item contained in the canvas frame : once cleared,
    the data will not reappear even if the show book statitsics button is clicked
    """
    for item in canvas1.get_tk_widget().find_all():
       canvas1.get_tk_widget().delete(item)

def clearcanvas2():
    """
    This function clears the data in canvas2 (contains the genrefigure graph)
    ! Problem : deletes every item contained in the canvas frame : once cleared,
    the data will not reappear even if the show book statitsics button is clicked
    """
    for item in canvas2.get_tk_widget().find_all():
       canvas2.get_tk_widget().delete(item)

bookfig = bookgraph(sorted_library_books,sorted_library_values)
genrefig = genregraph(sorted_genres,sorted_genre_values)

canvas1 = FigureCanvasTkAgg(bookfig,master=canvasframe)

canvas2 = FigureCanvasTkAgg(genrefig,master=canvasframe)

clearcanvas1_button = Button(master=canvasframe,text="Clear canvas",command=clearcanvas1)

clearcanvas2_button = Button(master=canvasframe,text="Clear canvas",command=clearcanvas2)

window.mainloop()

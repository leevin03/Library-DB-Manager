import sys
import book_dao

menu_options = {
    1: 'Add a Publisher',
    2: 'Add a Book',
    3: 'Edit a Book',
    4: 'Delete a Book',
    5: 'Search Books',
    6: 'Exit',
}
def print_menu():
    print()
    print("Please make a selection")
    for key in menu_options.keys():
        print (str(key)+'.', menu_options[key], end = "  ")
    print()
    print("The end of top-level options")
    print()

search_menu_options = {
    1: 'Search all books - title based',
    2: 'Search by publisher',
    3: 'Search by price range',
    4: 'Search by title and publisher'
}
def print_search_menu():
    print()
    print("Please make a selection")
    for key in search_menu_options.keys():
        print(str(key) + '.', search_menu_options[key], end="  ")
    print()
    print("The end of top-level options")
    print()

edit_menu_options = {
    1: 'Edit title',
    2: 'Edit published year',
    3: 'Edit book publisher',
    4: 'Edit previous edition of the book',
    5: 'Edit price of the book'
}
def print_edit_menu():
    print()
    print("Please make a selection")
    for key in edit_menu_options.keys():
        print(str(key) + '.', edit_menu_options[key], end="  ")
    print()
    print("The end of top-level options")
    print()

#search functions
def search_all_books():
    # Use a data access object (DAO) to 
    # abstract the retrieval of data from 
    # a data resource such as a database.
    results = book_dao.findAll()

    # Display results
    print("The following are the ISBNs and titles of all books.")
    for item in results:
        print(item['ISBN'], item['title'])
    print("The end of books.")

def search_by_title():
    title = input("What is the exact book title that you are looking for?\n")
    results = list(book_dao.findByTitle(title))
    # Display results
    if len(results) != 0:
        print("We found the following matching titles for you.")
        for item in results:
            print("ISBN: " + item['ISBN'], "Title: " + item['title'])
    else:
        print("The title you wanted does not exist in our database.")
    print("The end.")

def search_by_publisher():
    publisher = input("What is the book's publisher that you are looking for?\n")
    results = list(book_dao.findByPublisher(publisher))
    # Display results
    if len(results) != 0:
        print("We found the following matching titles for you.")
        for item in results:
            print("ISBN: " + item['ISBN'], "Title: " + item['title'], "Publisher: " + item['published_by'])
    else:
        print("The books published by the publisher you wanted does not exist in our database.")
    print("The end.")

def search_by_price_range():
    min_price = input("What is the minimum price you are looking for?\n")
    max_price = input("What is the maximum price you are looking for?\n")
    results = list(book_dao.findByPriceRange(min_price, max_price))
    # Display results
    if len(results) != 0:
        print("We found the following matching titles for you.")
        for item in results:
            print("ISBN: " + item['ISBN'], "Title: " + item['title'], "Price: " + str(item['price']))
    else:
        print("There are no books within the price range provided!")
    print("The end")

def search_by_title_publisher():
    title = input("What is the title of the book you are looking for?\n")
    publisher = input("What is the publisher of that book title?\n")
    results = list(book_dao.findByTitlePublisher(title, publisher))

    #Display results
    if len(results) != 0:
        print("We found the following matching titles for you.")
        for item in results:
            print("ISBN: " + item['ISBN'], "Title: " + item['title'], "Publisher: " + item['published_by'])
    else:
        print("There are no books with the title and publisher range provided!")
    print("The end")

#Insert new publisher to the publisher table
def insertNewPublisher():
    name = input("What is the name of the publisher you want to add?\n")
    phone = input("What is the phone number of the publisher you want to add?\n")
    city = input("What is the city of the publisher you want to add?\n")
    book_dao.insertNewPublisher(name, phone, city)
    print("Added new publisher!\n")


#Add a publisher to the database
def option1():
    insertNewPublisher()

#Add a book to the database
def option2():
    ISBN = input("What is the ISBN of the book you want to insert?\n")
    title = input("What is the title of the book you want to insert\n")
    year = input("When was the book published?\n")
    publisher = input("Who is the publisher of the book?\n")
    prev_edition = input("What is the previous edition of this book?\n")
    price = input("What is the price of this book?\n")
    book_dao.insertNewBook(ISBN, title, year, publisher, prev_edition, price)
    print("Added new book to the database!")

#Option 3: Edit a book
def option3():
    ISBN = input('What is the ISBN of the book you want to edit?\n')
    print_edit_menu()
    edit_option = ''
    try:
        edit_option = int(input('Enter your choice: '))
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
    except:
        print('Wrong input. Please enter a number ...')

    if edit_option == 1:
        newTitle = input("What is the edited title of the book?\n")
        book_dao.editBookTitle(ISBN, newTitle)
    elif edit_option == 2:
        newYear = int(input("What is the edited published year of the book?\n"))
        book_dao.editBookPublishedYear(ISBN, newYear)

    #Edit the publisher of the book
    #Insert the publisher if not in the DB
    elif edit_option == 3:
        newPublisher = input("What is the edited publisher of the book?\n")
        #search publisher
        result = book_dao.searchPublisher(newPublisher)
        publisher_count = 0
        for _ in result:
            publisher_count += 1
        #if publisher is already in database
        if publisher_count == 1:
            book_dao.editBookPublisher(ISBN, newPublisher)
        #if publisher is not in database
        elif publisher_count == 0:
            print("Publisher is not in database!")
            print("Please insert new publisher into database first!")
            #insert the new publisher first
            insertNewPublisher()
            book_dao.editBookPublisher(ISBN, newPublisher)
        print("Successfully edited book publisher")

    #If the edited previous edition of the book is not in database, it is invalid
    elif edit_option == 4:
        newPrevEdition = input("What is the edited previous edition of the book?\n")
        #search previous edition
        result = book_dao.searchBookISBN(newPrevEdition)
        book_count = 0
        for _ in result:
            book_count += 1
        if book_count == 1:
            book_dao.editBookPrevEdition(ISBN, newPrevEdition)
        else:
            print("Invalid ISBN previous book edition")
    elif edit_option == 5:
        newPrice = int(input("What is the edited price of the book?\n"))
        book_dao.editBookPrice(ISBN, newPrice)

#Option 4: Delete a book
def option4():
    ISBN = input("What is the ISBN of the book you want to delete?\n")
    book_dao.deleteBook(ISBN)
    print("Successfully deleted the book!")

#Option 5: Search for a book
def option5():
    # A sub-menu shall be printed
    # and prompt user selection
    print_search_menu()
    search_option = ''
    try:
        search_option = int(input('Enter your choice: '))
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
    except:
        print('Wrong input. Please enter a number ...')
    #Process different options for searching
    if search_option == 1:
        print("Search Option 1: all books were chosen.")
        search_all_books()
        search_by_title()

    elif search_option == 2:
        print("Search Option 2: search by publisher was chosen")
        search_by_publisher()

    elif search_option == 3:
        print("Search Option 3: search by price range was chosen")
        search_by_price_range()

    elif search_option == 4:
        print("Search Option 4: search by title and publisher was chosen")
        search_by_title_publisher()




if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        except:
            print('Wrong input. Please enter a number ...')

        # Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            option5()
        elif option == 6:
            print('Thanks your for using our database services! Bye')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 6.')












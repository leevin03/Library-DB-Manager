from pymongo_connector import collection, publisher_collection

#Search methods
def findAll():
    results = collection.find()
    return results

def findByTitle(book_title):
    results = collection.find({'title': book_title})
    return results

def findByPublisher(book_publisher):
    results = collection.find({'published_by': book_publisher})
    return results

def findByPriceRange(min_price, max_price):

    results = collection.find({'price':
                                   {"$gt": int(min_price),
                                    "$lt": int(max_price)
                                    }})
    return results

def findByTitlePublisher(title, publisher):
    results = collection.find({'title': title,
                               'published_by': publisher})
    return results

#Add a new book to the database
def insertNewBook(ISBN, title, year, publisher, prev_edition, price):

    new_book = {"ISBN": ISBN,
                "title": title,
                "year": year,
                "published_by": publisher,
                "previous_edition": prev_edition,
                "price": price}
    collection.insert_one(new_book)

#Add a new publisher
def insertNewPublisher(name, phone, city):
    new_publisher = {"name": name,
                     "phone": phone,
                     "city": city}
    publisher_collection.insert_one(new_publisher)

#Edit book functions
def editBookTitle(ISBN, newTitle):
    myQuery = {"ISBN": ISBN}
    newvalues = {"$set":
                     {"title": newTitle}
                }
    collection.update_one(myQuery, newvalues)

def editBookPublishedYear(ISBN, newYear):
    myQuery = {"ISBN": ISBN}
    newvalues = {"$set":
                     {"year": newYear}
                 }
    collection.update_one(myQuery, newvalues)

def editBookPublisher(ISBN, newPublisher):
    myQuery = {"ISBN": ISBN}
    newvalues = {"$set":
                     {"published_by": newPublisher}
                 }
    collection.update_one(myQuery, newvalues)

def editBookPrevEdition(ISBN, newPrevEdition):
    myQuery = {"ISBN": ISBN}
    newvalues = {"$set":
                     {"previous_edition": newPrevEdition}
                 }
    collection.update_one(myQuery, newvalues)

def editBookPrice(ISBN, newPrice):
    myQuery = {"ISBN": ISBN}
    newvalues = {"$set":
                     {"price": newPrice}
                 }
    collection.update_one(myQuery, newvalues)

##helper function for editing books
def searchBookISBN(ISBN):
    result = collection.find({'ISBN': ISBN })
    return result
def searchPublisher(Publisher):
    result = publisher_collection.find({'name': Publisher})
    return result

#delete a book from the table
def deleteBook(ISBN):
    collection.delete_one({'ISBN': ISBN})






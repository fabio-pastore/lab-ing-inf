from Book import *
from FastLibrary import *

class RemovableFastLibrary(FastLibrary):
    def __init__(self):
        FastLibrary.__init__(self)

    def remove_book(self, book):
        if not isinstance(book, Book):
            pass
        else:
            if book in self.find_books_by_author(book.author) and book in self.find_books_by_year(book.year):
                self.book_list[book.author].remove(book)
                self.book_list[book.year].remove(book)
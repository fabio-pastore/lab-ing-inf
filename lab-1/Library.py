from Book import *

class Library:
    def __init__(self):
        self.book_list = []
        pass

    def add_book(self, book):
        if isinstance(book, Book):
            self.book_list.append(book)
        else:
            pass

    def show_books(self):
        print("[ ", end='')
        for book in self.book_list:
            print(book, end=' ')
        print("]")

    def find_books_by_author(self, author):
        res = []
        for book in self.book_list:
            if book.author == author:
                res.append(book)
        return res
    
    def find_books_by_year(self, year):
        res = []
        for book in self.book_list:
            if book.year == year:
                res.append(book)
        return res





    
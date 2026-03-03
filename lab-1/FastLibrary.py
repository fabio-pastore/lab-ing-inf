from Book import *

class FastLibrary:
    def __init__(self):
        self.book_list = {}

    def add_book(self, book):
        if isinstance(book, Book):
            if book.author not in self.book_list.keys():
                self.book_list[book.author] = [book]
            else:
                self.book_list[book.author].append(book)
            if book.year not in self.book_list.keys():
                self.book_list[book.year] = [book]
            else:
                self.book_list[book.year].append(book)
        else:
            pass

    def show_books(self):
        print("[ ", end='')
        book_set = set()
        for l in list(self.book_list.values()):
            for book in l:
                if book not in book_set:
                    book_set.add(book)
                    print(book, end=' ')
        print("]")

    def find_books_by_author(self, author):
        ret = self.book_list.get(author)
        if ret is None:
            return []
        return ret
    
    def find_books_by_year(self, year):
        ret = self.book_list.get(year)
        if ret is None:
            return []
        return ret
    
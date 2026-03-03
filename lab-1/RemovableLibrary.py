from Library import *
from Book import *

class RemovableLibrary(Library):
    def __init__(self):
        Library.__init__(self) # chiama il costruttore della superclasse

    def remove_book(self, book):
        if not isinstance(book, Book):
            pass
        else:
            for b in self.book_list:
                if b == book:
                    self.book_list.remove(b)
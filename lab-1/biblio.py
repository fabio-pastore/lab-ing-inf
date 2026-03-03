from Book import *
from RemovableLibrary import *
from RemovableFastLibrary import *
from random import randint
from time import time

lib = RemovableLibrary()
flib = RemovableFastLibrary()

NUM_BOOKS = 100000

for i in range(NUM_BOOKS):
    b = Book(f"libro{i}", str(i), i, str(i))
    if i == 0:
        first_book = b
    lib.add_book(b)
    flib.add_book(b)

M = 1000

begin_timer = time()
for j in range(M):
    x = randint(0, NUM_BOOKS-1)
    lib.find_books_by_year(x)
end_timer = time()
print("Standard library took: " + str(round(end_timer - begin_timer, 3)) + " seconds!")

begin_timer = time()
for k in range(M):
    x = randint(0, NUM_BOOKS-1)
    flib.find_books_by_year(x)
end_timer = time()
print("Fast library took: " + str(round(end_timer - begin_timer, 3)) + " seconds!")

print()
input("Press ENTER to exit the process.")

class Book:
    def __init__(self, title, author, year, genre):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self):
        return ("[T: " + self.title + ", A: " + self.author + ", Y: " + str(self.year) + ", G: " + self.genre + "]")

    
    
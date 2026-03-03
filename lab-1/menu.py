from Book import *
from RemovableLibrary import *
from RemovableFastLibrary import *

# NOTA: possibili aggiunte future --> (i) check type dell'input per evitare errori di conversione a runtime
#                                     (ii) aggiungere ricerca per titolo e genere 

libraries = {}
lib_id = 1

print("Welcome to book-manager v1.0 by Fabio!")

while (True):
    print("Scegliere un'operazione:")
    print("1. Crea una nuova libreria")
    print("2. Seleziona una libreria su cui effettuare operazioni")
    print("3. Exit")
    choice = int(input("book-manager$ "))
    match choice:
        case 1:
            print("Seleziona il tipo di libreria da creare:")
            print("1. Standard")
            print("2. RemovableStandard")
            print("3. Fast")
            print("4. RemovableFast")
            lib_choice = int(input("book-manager$ "))
            match lib_choice:
                case 1:
                    lib = Library()
                case 2:
                    lib = RemovableLibrary()
                case 3:
                    lib = FastLibrary()
                case 4:
                    lib = RemovableFastLibrary()
                case _:
                    print("Scelta non valida.")
                    print()
                    continue

            libraries[lib_id] = lib
            print("Operazione completa con successo. ID libreria: " + str(lib_id))
            lib_id += 1
            print()

        case 2:
            if list(libraries.keys()) == []:
                print("Non sono ancora state registrate librerie sul sistema! Prima creane una.")
                print()
                continue

            print("Di seguito l'elenco degli ID delle librerie presenti sul sistema.")
            print(list(libraries.keys()))
            print("Inserire ID libreria:")
            selected_id_lib = int(input("book-manager$ "))
            if (libraries.get(selected_id_lib) is None or selected_id_lib < 0):
                print("Libreria inesistente. Controlla l'ID inserito.")
                print()
                continue

            else:
                selected_lib = libraries[selected_id_lib]
                can_remove = False
                print("Scegliere operazione da effettuare:")
                print("0. Torna al menu principale")
                print("1. Inserisci libro")
                print("2. Mostra libri")
                print("3. Cerca per autore")
                print("4. Cerca per anno")
                if (isinstance(selected_lib, (RemovableLibrary, RemovableFastLibrary))):
                    can_remove = True
                    print("5. Rimuovi libro")

                op_choice = int(input("book-manager$ "))
                match op_choice:
                    case 0:
                        continue # ritorna al menu principale

                    case 1:
                        print("Di seguito verranno richiesti alcuni dati inerenti al libro da inserire.")
                        print("Inserire il titolo del libro:")
                        title = input("book-manager$ ")
                        print("Inserire l'autore del libro:")
                        author = input("book-manager$ ")
                        print("Inserire l'anno di pubblicazione del libro:")
                        year = int(input("book-manager$ "))
                        print("Inserire il genere a cui appartiene il libro:")
                        genre = input("book-manager$ ")
                        book_to_insert = Book(title, author, year, genre)
                        selected_lib.add_book(book_to_insert)
                        print("Libro aggiunto con successo.")
                        print()

                    case 2:
                        print("Mostrando i contenuti della libreria con ID: " + str(selected_id_lib))
                        selected_lib.show_books()
                        print()

                    case 3:
                        print("Inserire l'autore per cui effettuare la ricerca:")
                        author_to_find = input("book-manager$ ")
                        search_res = selected_lib.find_books_by_author(author_to_find)
                        if search_res == []:
                            print("Impossibile trovare libri scritti dall'autore '" + author_to_find + "'" + " nella libreria con ID: " + str(selected_id_lib))
                            print()
                            continue

                        print("La ricerca ha prodotto i seguenti risultati:")
                        for book in search_res:
                            print(book)
                        print()

                    case 4:
                        print("Inserire l'anno per cui effettuare la ricerca:")
                        year_to_find = int(input("book-manager$ "))
                        search_res = selected_lib.find_books_by_year(year_to_find)
                        if search_res == []:
                            print("Impossibile trovare libri scritti nell'anno '" + str(year_to_find) + "' nella libreria con ID: " + str(selected_id_lib))
                            print()
                            continue

                        print("La ricerca ha prodotto i seguenti risultati:")
                        for book in search_res:
                            print(book)
                        print()

                    case 5:
                        if not can_remove: # la libreria selezionata non supporta la rimozione di libri!
                            print("Scelta non valida.")
                            print()
                            continue

                        selected_lib.show_books()
                        print("Di seguito verranno richiesti alcuni dati inerenti al libro da rimuovere. Consultare la lista di libri custoditi nella libreria per maggiori informazioni.")
                        print("Inserire il titolo del libro:")
                        title = input("book-manager$ ")
                        print("Inserire l'autore del libro:")
                        author = input("book-manager$ ")
                        print("Inserire l'anno di pubblicazione del libro:")
                        year = int(input("book-manager$ "))
                        print("Inserire il genere a cui appartiene il libro:")
                        found = False
                        genre = input("book-manager$ ")
                        list_books_year = selected_lib.find_books_by_year(year)
                        for b in list_books_year:
                            if b.title == title and b.genre == genre and b in selected_lib.find_books_by_author(author):
                                found = True
                                selected_lib.remove_book(b)

                        if not found:
                            print("ERRORE: libro non trovato!")
                            print()
                            continue

                        print("Rimozione completata con successo.")
                        print()

                    case _:
                        print("Scelta non valida.")
                        print()
                        continue

        case 3:
            print("Exiting with status code 0") # exit OK
            break
        case _:
            print("Scelta non valida.")
            print()
            continue
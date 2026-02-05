# ### Task 1: Generisanje niza od N random integera [Kompleksnost: 1]
# - [ ] Uneti broj N od korisnika
# - [ ] Generisati niz od N random celih brojeva u opsegu od 1 do 100
# - [ ] Ispisati generisani niz

# **Uputstvo za resavanje:**
# 1. Koristiti `input()` za unos broja N i konvertovati ga u `int`
# 2. Importovati `random` modul na pocetku fajla
# 3. Napraviti praznu listu
# 4. Koristiti `for` petlju od 0 do N:
#    - U svakoj iteraciji generisati random broj pomocu `random.randint(1, 100)`
#    - Dodati broj u listu pomocu `append()`
# 5. Prikazati generisani niz

# Importujemo random modul koji sadrži funkcije za generisanje slučajnih brojeva
import random

# Unos broja N od korisnika
# input() funkcija čita korisnički unos kao string
# int() konvertuje taj string u ceo broj (integer)
N = int(input("Unesite broj N: "))

# Kreiramo praznu listu koja će čuvati generisane random brojeve
niz = []

# For petlja koja se izvršava N puta (od 0 do N-1)
# range(N) generiše sekvencu brojeva od 0 do N-1
# Promenljiva i predstavlja trenutnu iteraciju (0, 1, 2, ..., N-1)
for i in range(N):
    # random.randint(1, 100) generiše slučajan ceo broj između 1 i 100 (uključujući obe granice)
    # Generisani broj čuvamo u promenljivoj "broj"
    broj = random.randint(1, 100)

    # append() metoda dodaje element na kraj liste
    # Svaki generisani broj dodajemo u našu listu "niz"
    niz.append(broj)

# Ispisujemo konačan generisani niz
# print() funkcija prikazuje tekst i sadržaj liste na ekranu
print("Generisani niz:", niz)
lista = []

for i in range(10):
    broj = int(input("Unesi broj: "))
    lista.append(broj)
#ovaj deo nas pita 10 puta da unesemo broj po zelji i onda appenduje sve brojeve u listu
proizvod = 1
for x in lista:
    proizvod *= x
#ovo mnozi sve elemente iz liste
print("Lista:", lista)
print("Proizvod elemenata:", proizvod)

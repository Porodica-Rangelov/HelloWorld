print("Dobrodosli u sortiranje elemenata niza - rastuće")

niz = []

for i in range(10):
    broj = int(input("Unesi broj: "))
    niz.append(broj)

print("Pre sortiranja:", niz)

n = len(niz)
# algoritam je tacno implementiran, output je tacan
# ali 'i' ne treba da ide do 'n', vec do 'n-1', jer ako ide do 'n', u poslednoj iteraciji se element poredi sam sa sobom
# to nije optimalno
for i in range(n): 
    for j in range(0, n - i - 1):
        if niz[j] > niz[j + 1]:
            temp = niz[j]
            niz[j] = niz[j + 1]
            niz[j + 1] = temp

print("Posle sortiranja:", niz)

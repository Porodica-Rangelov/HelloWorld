print("Dobrodosli u sortiranje elemenata niza - rastuće")

niz = []

for i in range(10):
    broj = int(input("Unesi broj: "))
    niz.append(broj)

print("Pre sortiranja:", niz)

n = len(niz)
for i in range(n):
    for j in range(0, n - i - 1):
        if niz[j] > niz[j + 1]:
            temp = niz[j]
            niz[j] = niz[j + 1]
            niz[j + 1] = temp

print("Posle sortiranja:", niz)

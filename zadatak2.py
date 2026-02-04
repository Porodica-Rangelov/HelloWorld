print("Dobrodosli u sume prvih 10 brojeva")

suma = 0
for i in range(1, 11):
    suma += i

print("Suma prirodnih brojeva od 1 do 10: ", suma)

suma = 0
for i in range(1, 11):
    if i % 2 == 0:
        suma += i

print("Suma parnih brojeva od 1 do 10: ", suma)

suma = 0
for i in range(1, 11):
    if i % 2 != 0:
        suma += i        

print("Suma neparnih brojeva od 1 do 10: ", suma)
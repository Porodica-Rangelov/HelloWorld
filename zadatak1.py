#Zadatak 1)
print("Dobrodosli u Suma cifara visecifrenog broja")
broj = int(input("Unesi visecifreni broj: "))
suma = 0

# ovo je dobro, Djole
# petlja koja ide kroz sve cifre broja
while broj > 0:
    cifra = broj % 10
    suma += cifra
    broj //= 10

print("Suma cifara je:", suma)
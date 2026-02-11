import random

lista = []

for i in range(10):
    numero = random.randint(1, 100)
    lista.append(numero)

print(lista)

print("Lista con indices:")
for i in range(len(lista)):
    print(f"Indx {i}: {lista[i]}")
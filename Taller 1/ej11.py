import random

listaOriginal = []
for i in range(10):
    listaOriginal.append(random.randint(1, 21))

print("Lista: ")
for i in range(len(listaOriginal)):
    print(listaOriginal[i], end=" ")

listaMayores = []
for i in range(len(listaOriginal)):
    if listaOriginal[i] > 10:
        listaMayores.append(listaOriginal[i])

print("\n\nNúmeros mayores a 10: ")
for i in range(len(listaMayores)):
    print(listaMayores[i], end=" ")
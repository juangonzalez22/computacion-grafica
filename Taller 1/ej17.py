import random

def average(numList):
    sum = 0
    for i in range(len(numList)):
        sum += numList[i]
    return sum / len(numList)


lista = []
largo = random.randint(3, 21)

for i in range(largo):
    numero = random.randint(1, 100)
    lista.append(numero)

for i in range(len(lista)):
    print(f"{lista[i]} ", end="")

print()
print(f"Promedio: {average(lista)}")
notas = [0, 0, 0, 0, 0]

for i in range(len(notas)):
    notas[i] = float(input(f"Ingrese la nota {i + 1}: "))


maxNota = max(notas)
minNota = min(notas)

print("\nNotas ingresadas:")
for i in range(len(notas)):
    print(f"Nota {i + 1}: {notas[i]}")

print(f"Nota máxima: {maxNota}")
print(f"Nota mínima: {minNota}")
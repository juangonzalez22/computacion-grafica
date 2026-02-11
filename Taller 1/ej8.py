numero = int(input("Ingrese un número (0 para terminar): "))
sumatoria = 0

while numero != 0:
    sumatoria += numero
    numero = int(input("Ingrese un número (0 para terminar): "))

print("\nResultados:")
print("La sumatoria de los números ingresados es:", sumatoria)

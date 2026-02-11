año = int(input("Ingrese un año: "))

esBisiesto = (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)

print("\nResultados:")
print("¿El año es bisiesto?", esBisiesto)
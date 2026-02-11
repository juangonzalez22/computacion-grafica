n1 = float(input("Ingrese el primer número: "))
n2 = float(input("Ingrese el segundo número: "))


print("\nResultados:")
print("Suma:", n1 + n2)
print("Resta:", n1 - n2)
print("Multiplicación:", n1 * n2)
if n2 != 0 or n2 != 0.0:
    print("División real:", n1 / n2)
    print("División entera:", n1 // n2)
    print("Módulo:", n1 % n2)
else:
    print("División real: Error, división por cero")
    print("División entera: Error, división por cero")
    print("Módulo: Error, división por cero")
print("Potencia:", n1 ** n2)
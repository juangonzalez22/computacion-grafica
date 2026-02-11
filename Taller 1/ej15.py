def area(b, h):
    return (b * h) / 2

base = float(input("Ingrese la base del triángulo: "))
altura = float(input("Ingrese la altura del triángulo: "))
resultado = area(base, altura)
print("El área del triángulo es:", resultado)
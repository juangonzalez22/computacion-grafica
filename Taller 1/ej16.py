def isEven(num):
    return num % 2 == 0

number = int(input("Ingrese un número: "))
if isEven(number):
    print("El número es par.")
else:
    print("El número es impar.")
# Datos personales

nombre = str(input("Ingrese su nombre completo: "))
edad = int(input("Ingrese su edad: "))
estatura = float(input("Ingrese su estatura en metros: "))
estado = bool(input("¿Es usted estudiante? (True/False): "))

# Imprimir los datos personales
print("\nDatos personales:")
print("Nombre:", nombre)
print("Edad:", edad)
print("Estatura:", estatura, "metros")
print("¿Es estudiante?", estado)
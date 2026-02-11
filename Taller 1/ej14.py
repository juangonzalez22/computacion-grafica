# Ingresar 3 contactos en un diccionario con nombre y teléfono

contactos = {  
}

for i in range(3):
    nombre = input(f"Ingrese el nombre del contacto {i+1}: ")
    telefono = input(f"Ingrese el teléfono del contacto {i+1}: ")
    contactos[nombre] = telefono

print("Ingrese el nombre del contacto que desea buscar:")
nombre_buscar = str(input())
if nombre_buscar in contactos:
    print("El teléfono de", nombre_buscar, "es:", contactos[nombre_buscar])
else:
    print("El contacto no se encuentra en la lista.")
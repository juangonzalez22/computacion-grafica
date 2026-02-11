nota = float(input("Ingrese la nota: "))
resultado = ""

if nota >= 4.5 and nota <= 5.0:
    resultado = "Excelente"
elif nota >= 3.5 and nota < 4.5:
    resultado = "Buena"
elif nota >= 3.0 and nota < 3.5:
    resultado = "Regular"
elif nota < 3.0 and nota >= 0:
    resultado = "Reprobado"
else:
    resultado = "Nota inválida"

print("\nResultados:")
print("La nota ingresada es:", nota)
print("El resultado es:", resultado)
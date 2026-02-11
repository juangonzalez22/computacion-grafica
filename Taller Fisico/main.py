from dotproduct import dot_product, angle_between_vectors
from freefall import time_to_fall
from projectile import max_reach, max_height
from rectmovement import movement_in_line
from speedconv import convert_speed
from vectoraddition import vector_addition
import colorama

import scipy.constants as sc
gravity = sc.g



colorama.init(autoreset=True)
PROMPT = colorama.Style.BRIGHT + colorama.Fore.CYAN
MENU = colorama.Style.BRIGHT + colorama.Fore.GREEN
RESULT = colorama.Style.BRIGHT + colorama.Fore.MAGENTA
ERROR = colorama.Style.BRIGHT + colorama.Fore.RED
HINT = colorama.Style.DIM + colorama.Fore.YELLOW

def clean_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def enter_to_continue(text="Presiona Enter para continuar..."):
    input(PROMPT + text)

def input_float(prompt):
    while True:
        valor = input(PROMPT + prompt)
        try:
            valor_norm = valor.replace(',', '.')
            return float(valor_norm)
        except ValueError:
            print(ERROR + "Error, no se ha ingresado un número. Intente de nuevo.")

def input_int(prompt, min_value=None, max_value=None):
    while True:
        valor = input(PROMPT + prompt)
        try:
            i = int(valor)
            if min_value is not None and i < min_value:
                print(ERROR + f"Error: el número debe ser mayor o igual a {min_value}.")
                continue
            if max_value is not None and i > max_value:
                print(ERROR + f"Error: el número debe ser menor o igual a {max_value}.")
                continue
            return i
        except ValueError:
            print(ERROR + "Error, no se ha ingresado un número entero. Intente de nuevo.")

isActive = True

clean_console()

while isActive:
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "Taller de física en Python")
    print(colorama.Style.BRIGHT + colorama.Fore.WHITE + "-" * 30)

    print(MENU + "Seleccione una opción:")
    print(MENU + "1. Cálculo de tiempo de caída libre")
    print(MENU + "2. Conversión de unidades de velocidad")
    print(MENU + "3. Cálculo de desplazamiento en línea recta")
    print(MENU + "4. Suma de vectores")
    print(MENU + "5. Producto escalar de dos vectores")
    print(MENU + "6. Cálculo de alcance máximo y altura máxima de un proyectil")
    print(MENU + "7. Salir")
    print(colorama.Style.BRIGHT + colorama.Fore.WHITE + "-" * 30)
    choice = input(PROMPT + "Ingrese el número de la opción deseada: ")
    if not choice.isdigit():
        clean_console()
        print(ERROR + "Error, no se ha ingresado un número. Intente de nuevo.")
        enter_to_continue()
        clean_console()
        continue

    if choice == '1':
        clean_console()
        height = input_float("Ingrese la altura desde la que se deja caer el objeto (en metros): ")
        time = time_to_fall(height, gravity)
        print(RESULT + f"El tiempo que tarda el objeto en caer es: {time:.2f} segundos")
        enter_to_continue()
        clean_console()
    elif choice == '2':
        clean_console()
        input_speed = input_float("Ingrese la velocidad a convertir: ")
        conversion_type = input_int("Ingrese 1 para convertir de m/s a km/h, 2 para convertir de km/h a m/s: ", min_value=1, max_value=2)
        converted_speed = convert_speed(input_speed, conversion_type)
        if conversion_type == 1:
            print(RESULT + f"{input_speed} m/s es igual a {converted_speed:.2f} km/h")
        else:
            print(RESULT + f"{input_speed} km/h es igual a {converted_speed:.2f} m/s")
        enter_to_continue()
        clean_console()
    elif choice == '3':
        clean_console()
        start_speed = input_float("Ingrese la velocidad inicial (en m/s): ")
        acceleration = input_float("Ingrese la aceleración (en m/s2): ")
        time = input_float("Ingrese el tiempo (en segundos): ")
        distance = movement_in_line(start_speed, acceleration, time)
        print(RESULT + f"El desplazamiento en línea recta es: {distance:.2f} metros")
        enter_to_continue()
        clean_console()
    elif choice == '4':
        clean_console()
        size = input_int("Ingrese el tamaño de los vectores: ", min_value=1)
        vector1 = []
        vector2 = []
        for i in range(size):
            val1 = input_float(f"Ingrese el elemento {i+1} del primer vector: ")
            vector1.append(val1)
            val2 = input_float(f"Ingrese el elemento {i+1} del segundo vector: ")
            vector2.append(val2)
        result_vector = vector_addition(vector1, vector2)
        print(RESULT + "El vector resultante es: [", end="")
        for i in range(len(result_vector)):
            if i != len(result_vector) - 1:
                print(RESULT + f"{result_vector[i]}, ", end="")
            else:
                print(RESULT + f"{result_vector[i]}]", end="\n")
        enter_to_continue()
        clean_console()
    elif choice == '5':
        clean_console()
        size = input_int("Ingrese el tamaño de los vectores: ", min_value=1)
        vector1 = []
        vector2 = []
        for i in range(size):
            val1 = input_float(f"Ingrese el elemento {i+1} del primer vector: ")
            vector1.append(val1)
            val2 = input_float(f"Ingrese el elemento {i+1} del segundo vector: ")
            vector2.append(val2)
        result = dot_product(vector1, vector2)
        angle = angle_between_vectors(vector1, vector2)
        print(RESULT + f"El producto escalar de los dos vectores es: {result:.2f}")
        print(RESULT + f"El ángulo entre los dos vectores es: {angle:.2f} grados")
        enter_to_continue()
        clean_console()
    elif choice == '6':
        clean_console()
        initial_speed = input_float("Ingrese la velocidad inicial del proyectil (en m/s): ")
        launch_angle = input_float("Ingrese el ángulo de lanzamiento (en grados): ")
        reach = max_reach(initial_speed, launch_angle, gravity)
        height = max_height(initial_speed, launch_angle, gravity)
        print(RESULT + f"El alcance máximo del proyectil es: {reach:.2f} metros")
        print(RESULT + f"La altura máxima del proyectil es: {height:.2f} metros")
        enter_to_continue()
        clean_console()
    elif choice == '7':
        isActive = False
        print(MENU + "Saliendo del programa. ¡Hasta luego!")
        enter_to_continue()
        clean_console()
    else:
        clean_console()
        print(ERROR + "Opción no válida. Por favor, intente de nuevo.")
        enter_to_continue()
        clean_console()


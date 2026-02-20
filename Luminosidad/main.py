import numpy as np
import matplotlib.pyplot as plt

url = input("Ingrese la ruta o URL de la imagen: ")
imagen = plt.imread(url)

brillo = float(input("Ingrese el valor de brillo (ej: 40 o 0.2): "))

if imagen.max() <= 1.0:
    imagen_luminosa = np.clip(imagen + brillo, 0, 1)
else:
    imagen_luminosa = np.clip(imagen + brillo, 0, 255).astype(np.uint8)

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.imshow(imagen)
plt.title("Imagen Original")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(imagen_luminosa)
plt.title("Imagen con Brillo Ajustado")
plt.axis("off")

plt.tight_layout()
plt.show()
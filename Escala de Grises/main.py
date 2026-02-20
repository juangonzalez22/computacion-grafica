import numpy as np
import matplotlib.pyplot as plt

url = input("Ingrese la URL de la imagen: ")
imagen = plt.imread(url)


gris = 0.299*imagen[:,:,0] + 0.587*imagen[:,:,1] + 0.114*imagen[:,:,2]

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.imshow(imagen)
plt.title("Imagen Original")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(gris)
plt.title("Escala de Grises (Promedio)")
plt.axis("off")

plt.tight_layout()
plt.show()
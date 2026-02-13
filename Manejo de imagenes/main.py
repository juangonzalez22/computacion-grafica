import matplotlib.pyplot as plt
import numpy as np

ruta = "images/gengar2          .png"
imagen = plt.imread(ruta)

plt.figure(figsize=(8,8))

# Imagen original
plt.subplot(2, 2, 1)
plt.imshow(imagen)
plt.axis("off")
plt.title("Imagen Original")

# Capa Roja
CapaRoja = np.copy(imagen)
CapaRoja[:, :, 1] = CapaRoja[:, :, 2] = 0
plt.subplot(2, 2, 2)
plt.imshow(CapaRoja)
plt.axis("off")
plt.title("Capa Roja")

# Capa Verde
CapaVerde = np.copy(imagen)
CapaVerde[:, :, 0] = CapaVerde[:, :, 2] = 0

plt.subplot(2, 2, 3)
plt.imshow(CapaVerde)
plt.axis("off")
plt.title("Capa Verde")

# Capa Azul
CapaAzul = np.copy(imagen)
CapaAzul[:, :, 0] = CapaAzul[:, :, 1] = 0

plt.subplot(2, 2, 4)
plt.imshow(CapaAzul)
plt.axis("off")
plt.title("Capa Azul")

plt.show()


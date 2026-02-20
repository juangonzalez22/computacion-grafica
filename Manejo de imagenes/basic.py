import matplotlib.pyplot as plt
import numpy as np

ruta = "images/gengar.jpg"
imagen = plt.imread(ruta)

fig, axes = plt.subplots(3, 3, figsize=(10, 10))

# Imagen Original
axes[0, 0].imshow(imagen)
axes[0, 0].set_title("Imagen Original")
axes[0, 0].axis("off")

# Capa Roja
CapaRoja = np.copy(imagen)
CapaRoja[:, :, 1] = 0
CapaRoja[:, :, 2] = 0
axes[0, 1].imshow(CapaRoja)
axes[0, 1].set_title("Capa Roja")
axes[0, 1].axis("off")

# Capa Verde
CapaVerde = np.copy(imagen)
CapaVerde[:, :, 0] = 0
CapaVerde[:, :, 2] = 0
axes[0, 2].imshow(CapaVerde)
axes[0, 2].set_title("Capa Verde")
axes[0, 2].axis("off")

# Capa Azul
CapaAzul = np.copy(imagen)
CapaAzul[:, :, 0] = 0
CapaAzul[:, :, 1] = 0
axes[1, 0].imshow(CapaAzul)
axes[1, 0].set_title("Capa Azul")
axes[1, 0].axis("off")

# Capa Cyan
CapaCyan = np.copy(imagen)
CapaCyan[:, :, 0] = 0
axes[1, 1].imshow(CapaCyan)
axes[1, 1].set_title("Capa Cyan")
axes[1, 1].axis("off")

# Capa Magenta
CapaMagenta = np.copy(imagen)
CapaMagenta[:, :, 1] = 0
axes[1, 2].imshow(CapaMagenta)
axes[1, 2].set_title("Capa Magenta")
axes[1, 2].axis("off")

# Capa Amarilla
CapaAmarilla = np.copy(imagen)
CapaAmarilla[:, :, 2] = 0
axes[2, 0].imshow(CapaAmarilla)
axes[2, 0].set_title("Capa Amarilla")
axes[2, 0].axis("off")

# Imagen invertida
Negativo = np.copy(imagen)
if Negativo.shape[2] == 4:
    Negativo[:, :, :3] = 1 - Negativo[:, :, :3]
else:
    Negativo = 255 - Negativo
axes[2, 1].imshow(Negativo)
axes[2, 1].set_title("Imagen Invertida")
axes[2, 1].axis("off")

plt.tight_layout()
plt.show()

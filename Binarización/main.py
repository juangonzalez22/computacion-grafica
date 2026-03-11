import matplotlib.pyplot as plt
import numpy as np

img_url = input("Ingrese la URL de la imagen: ")
img = plt.imread(img_url)

img_gray = 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]

threshold = 128

img_binary = np.where(img_gray > threshold, 255, 0).astype(np.uint8)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Imagen Original")
plt.imshow(img)
plt.axis('off')
plt.subplot(1, 2, 2)
plt.title("Imagen Binarizada")
plt.imshow(img_binary, cmap='gray')
plt.axis('off')
plt.show()
import numpy as np
import matplotlib.pyplot as plt

first = input("Ingrese la ruta de la primera imagen: ")
second = input("Ingrese la ruta de la segunda imagen: ")
factor = float(input("Ingrese el factor de mezcla (0.0 a 1.0): "))

img1 = plt.imread(first)
img2 = plt.imread(second)

def normalize(img):
    if img.dtype in [np.float32, np.float64]:
        return (img * 255).astype(np.uint8)
    return img.astype(np.uint8)

img1 = normalize(img1)
img2 = normalize(img2)

height = min(img1.shape[0], img2.shape[0])
width = min(img1.shape[1], img2.shape[1])
channels = min(img1.shape[2], img2.shape[2])

img1_resized = img1[:height, :width, :channels]
img2_resized = img2[:height, :width, :channels]

alpha = factor
fused_img = (alpha * img1_resized + (1 - alpha) * img2_resized).astype(np.uint8)

plt.imshow(fused_img)
plt.axis('off')
plt.show()

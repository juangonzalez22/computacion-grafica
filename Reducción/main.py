import matplotlib.pyplot as plt
import numpy as np

img_route = input("Ingrese la URL de la imagen: ")
img = plt.imread(img_route)

factor = 1

plt.figure(figsize=(10, 10))


for i in range(1, 5):
    factor *= 2
    reduced_img = img[::factor, ::factor]
    plt.subplot(2   , 2, i)
    plt.imshow(reduced_img)
    plt.title(f"reducción: {factor}")
    plt.axis('off')


plt.show()


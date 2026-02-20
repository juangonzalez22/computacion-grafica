import numpy as np
import matplotlib.pyplot as plt

red = input("Ingrese la ruta de la imagen roja: ")
green = input("Ingrese la ruta de la imagen verde: ")
blue = input("Ingrese la ruta de la imagen azul: ")

red_image = plt.imread(red)
blue_image = plt.imread(blue)
green_image = plt.imread(green)

finalImage = np.copy(red_image)
finalImage[:, :, 0] = red_image[:, :, 0]
finalImage[:, :, 1] = green_image[:, :, 1]
finalImage[:, :, 2] = blue_image[:, :, 2]

plt.imshow(finalImage)
plt.axis('off')
plt.show()
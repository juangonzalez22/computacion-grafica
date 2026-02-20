import numpy as np
import matplotlib.pyplot as plt

#route = input("Ingrese la ruta de la imagen: ")
#image = plt.imread(route)

def togreen(image):
    green = np.copy(image)
    green[:, :, 0] = 0
    green[:, :, 2] = 0
    return green

#plt.imshow(togreen(image))
#plt.axis('off')
#plt.show()
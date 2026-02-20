import numpy as np
import matplotlib.pyplot as plt

#route = input("Ingrese la ruta de la imagen: ")
#image = plt.imread(route)

def tomagenta(image):
    magenta = np.copy(image)
    magenta[:, :, 1] = 0
    return magenta

#plt.imshow(tomagenta(image))
#plt.axis('off')
#plt.show()
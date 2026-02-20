import numpy as np
import matplotlib.pyplot as plt

#route = input("Ingrese la ruta de la imagen: ")
#image = plt.imread(route)

def toblue(image):
    blue = np.copy(image)
    blue[:, :, 0] = 0
    blue[:, :, 1] = 0
    return blue

#plt.imshow(toblue(image))
#plt.axis('off')
#plt.show()
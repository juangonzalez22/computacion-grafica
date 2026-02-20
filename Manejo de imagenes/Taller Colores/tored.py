import numpy as np
import matplotlib.pyplot as plt

#route = input("Ingrese la ruta de la imagen: ")
#image = plt.imread(route)

def tored(image):
    red = np.copy(image)
    red[:, :, 1] = 0
    red[:, :, 2] = 0
    return red

#plt.imshow(tored(image))
#plt.axis('off')
#plt.show()
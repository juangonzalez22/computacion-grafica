import numpy as np
import matplotlib.pyplot as plt

#route = input("Ingrese la ruta de la imagen: ")
#image = plt.imread(route)

def tocyan(image):
    cyan = np.copy(image)
    cyan[:, :, 0] = 0
    return cyan

#plt.imshow(tocyan(image))
#plt.axis('off')
#plt.show()
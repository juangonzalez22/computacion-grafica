import numpy as np
import matplotlib.pyplot as plt

#route = input("Ingrese la ruta de la imagen: ")
#image = plt.imread(route)

def toyellow(image):
    yellow = np.copy(image)
    yellow[:, :, 2] = 0
    return yellow

#plt.imshow(toyellow(image))
#plt.axis('off')
#plt.show()
import numpy as np
import matplotlib.pyplot as plt

route = input("Ingrese la ruta de la imagen: ")
image = plt.imread(route)

def inversor(image):
    negative = np.copy(image)
    if negative.shape[2] == 4:
        return 1 - negative[:, :, :3]
    else:
        return 255 - negative
    
plt.imshow(inversor(image))
plt.axis('off')
plt.show()
import numpy as np
import matplotlib.pyplot as plt
import os
from tored import tored
from toblue import toblue
from togreen import togreen

route = input("Ingrese la ruta de la imagen: ")
image = plt.imread(route)

red = tored(image)
blue = toblue(image)
green = togreen(image)

# Guardar las imágenes resultantes
base_name = os.path.splitext(os.path.basename(route))[0]
plt.imsave(f"{base_name}_red.png", red)
plt.imsave(f"{base_name}_blue.png", blue)
plt.imsave(f"{base_name}_green.png", green)
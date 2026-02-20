import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

route1 = input("Ingrese la ruta de la primera imagen: ")
route2 = input("Ingrese la ruta de la segunda imagen: ")

image1=plt.imread(route1)
image2=plt.imread(route2)

print("dtype de la imagen 1: ", image1.dtype)
print("dtype de la imagen 2: ", image2.dtype)

h, w, c = image1.shape
image2 = np.array(Image.fromarray(image2).resize((w, h)))


A = image1.astype(np.float32)
B = image2.astype(np.float32)

fusion = (A + B) / 2
fusion = np.clip(fusion, 0, 255).astype(np.uint8)

plt.imshow(fusion)
plt.axis('off')
plt.title('Imagen Fusionada')
plt.show()
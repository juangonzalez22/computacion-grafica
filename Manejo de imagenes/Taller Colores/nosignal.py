import numpy as np
import matplotlib.pyplot as plt

image = np.zeros((7, 12, 3), dtype=np.uint8)

red = [255, 0, 0]
blue = [0, 0, 255]
green = [0, 255, 0]
cyan = [0, 255, 255]
magenta = [255, 0, 255]
yellow = [255, 255, 0]

image[0:5, 0:2] = yellow
image[0:5, 2:4] = cyan
image[0:5, 4:6] = green
image[0:5, 6:8] = magenta
image[0:5, 8:10] = red
image[0:5, 10:12] = blue

for i in range(5, 7):
    for j in range(0, 12):
        image[i, j] = [255 - (j * 255 // 11), 255 - (j * 255 // 11), 255 - (j * 255 // 11)]

plt.imshow(image)
plt.axis('off')
plt.show()
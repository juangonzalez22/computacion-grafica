import numpy as np
import matplotlib.pyplot as plt

colors = np.zeros((3, 3, 3), dtype=np.uint8)

red = [255, 0, 0]
blue = [0, 0, 255]
green = [0, 255, 0]
cyan = [0, 255, 255]
magenta = [255, 0, 255]
yellow = [255, 255, 0]
white = [255, 255, 255]
black = [0, 0, 0]
gray = [128, 128, 128]

colors[0, 0] = cyan
colors[0, 1] = white
colors[0, 2] = red
colors[1, 0] = magenta
colors[1, 1] = gray
colors[1, 2] = green
colors[2, 0] = yellow
colors[2, 1] = black
colors[2, 2] = blue

plt.imshow(colors)
plt.axis('off')
plt.show()

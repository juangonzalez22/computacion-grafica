import numpy as np
import matplotlib.pyplot as plt

mario = np.zeros((16, 14, 3), dtype=np.uint8)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
gray = (128, 128, 128)
skin = (255, 204, 153)
brown = (139, 69, 19)
white = (255, 255, 255)

mario[:,:]=white

mario[15, 0:4] = brown
mario[14, 1:4] = brown
mario[15, 8:12] = brown
mario[14, 8:11] = brown
mario[2, 2:5] = brown
mario[3:5, 3] = brown
mario[4, 4] = brown
mario[3:6, 1] = brown
mario[5, 2] = brown


mario[13, 2:5] = blue
mario[13, 7:10] = blue
mario[12, 2:10] = blue
mario[11, 3:9] = blue
mario[10, 3] = blue
mario[10, 5:7] = blue
mario[10, 8] = blue
mario[7:10, 4] = blue
mario[8:10, 7] = blue

mario[10, 4] = yellow
mario[10, 7] = yellow
mario[9, 5:7] = blue

mario[10, 2] = red
mario[10, 9] = red
mario[9, 0:4] = red
mario[9, 8:12] = red
mario[8, 1:4] = red
mario[8, 5:7] = red
mario[8, 8:11] = red
mario[7, 2:4] = red
mario[7, 5:9] = red
mario[0, 3:9] = red
mario[1, 2:12] = red

mario[12, 0:2] = skin
mario[12, 10:12] = skin
mario[11, 0:3] = skin
mario[11, 9:12] = skin
mario[10, 0:2] = skin
mario[10, 10:12] = skin

mario[6, 3:11] = skin
mario[5, 3:8] = skin
mario[3:5, 2] = skin    
mario[4, 5:9] = skin
mario[3, 4:8] = skin
mario[2, 5:8] = skin
mario[2, 9] = skin
mario[3, 9:12] = skin
mario[4, 10:13] = skin

mario[2:4 ,8] = black
mario[5, 8:12] = black
mario[4, 9] = black

plt.imshow(mario)
plt.axis('off')
plt.show()
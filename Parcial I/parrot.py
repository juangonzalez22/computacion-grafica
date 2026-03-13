import matplotlib.pyplot as plt
import numpy as np

parrot = np.zeros((17, 17, 3), dtype=np.uint8)

red =(207, 52, 50)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (254, 235, 53)
blue = (36, 168, 243)
green = (80, 174, 77)
orange = (246, 169, 37)
beige = (254, 224, 188)
purple = (154, 42, 178)

# Inicializar todo en blanco
parrot[:, :] = white

# Pixeles rojos
parrot[14:16, 12] = red
parrot[12, 7:9] = red
parrot[10:12, 6:8] = red
parrot[7:10, 5:7] = red
parrot[7,7] = red
parrot[7,10] = red
parrot[6, 6:10] = red
parrot[5, 7:10] = red
parrot[2:5, 8] = red
parrot[1, 5:8] = red
parrot[2,4:6] = red

# Pixeles naranjas
parrot[13, 6:9] = orange
parrot[3:5, 4:6] = orange
parrot[5,4] = orange

# Pixeles amarillos
parrot[9, 8:12] = yellow
parrot[8, 7:11] = yellow
parrot[7, 8:10] = yellow

# Pixeles verdes
parrot[10, 9:12] = green
parrot[11, 11:13]= green

# Pixeles azules
parrot[9,7] = blue
parrot[10:12, 8] = blue
parrot[12, 9:11] = blue
parrot[13, 10:13] = blue
parrot[14,11] = blue

# Pixeles morados
parrot[11, 9:11] = purple
parrot[12, 11:13] = purple

# Pixeles beige
parrot[6,5] = beige
parrot[4:6, 6] = beige  
parrot[2:5, 7] = beige
parrot[2,6] = beige

# Pixeles negros
parrot[3,6] = black
parrot[5,5] = black

plt.imshow(parrot)
plt.axis('off')
plt.show()


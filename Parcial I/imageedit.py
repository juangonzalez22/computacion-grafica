import imagelib as ilib
import matplotlib.pyplot as plt
import numpy as np

url_1 = "imagen_1.jpg"
url_2 = "imagen_2.png"

img_1 = plt.imread(url_1)
img_2 = plt.imread(url_2)

# Como la librería propia usa -1 y 1, no -255 y 255, se normalizan las imágenes a ese rango
shiny = 55/255
dark = -50/255

shiny_1 = ilib.adjust_brightness(img_1, shiny)
dark_1 = ilib.adjust_brightness(img_1, dark)

shiny_2 = ilib.adjust_brightness(img_2, shiny)
dark_2 = ilib.adjust_brightness(img_2, dark)

rgb_1 = ilib.extract_rgb_channels(img_1)
rgb_2 = ilib.extract_rgb_channels(img_2)
cmyk_1 = ilib.extract_cymk_channels(img_1)
cmyk_2 = ilib.extract_cymk_channels(img_2)

red_1 = rgb_1[0]
red_2 = rgb_2[0]

magenta_1 = cmyk_1[1]
magenta_2 = cmyk_2[1]

monochrome_1 = ilib.monochrome(img_1)
monochrome_2 = ilib.monochrome(img_2)


# Mostrar todas las 10 imágenes
fig, axes = plt.subplots(2, 6, figsize=(20, 8))
axes[0, 0].imshow(img_1)
axes[0, 0].set_title("Imagen 1")

axes[0, 1].imshow(shiny_1)
axes[0, 1].set_title("Brillo Aumentado +55")

axes[0, 2].imshow(dark_1)
axes[0, 2].set_title("Brillo Disminuido -50")

axes[0, 3].imshow(red_1)
axes[0, 3].set_title("Canal Rojo")

axes[0, 4].imshow(magenta_1)
axes[0, 4].set_title("Canal Magenta")

axes[0, 5].imshow(monochrome_1, cmap="gray")
axes[0, 5].set_title("Blanco y negro")

axes[1, 0].imshow(img_2)
axes[1, 0].set_title("Imagen 2")

axes[1, 1].imshow(shiny_2)
axes[1, 1].set_title("Brillo Aumentado +55")

axes[1, 2].imshow(dark_2)
axes[1, 2].set_title("Brillo Disminuido -50")

axes[1, 3].imshow(red_2)
axes[1, 3].set_title("Canal Rojo")

axes[1, 4].imshow(magenta_2)
axes[1, 4].set_title("Canal Magenta")

axes[1, 5].imshow(monochrome_2, cmap="gray")
axes[1, 5].set_title("Blanco y negro")

for ax in axes.flatten():
    ax.axis("off")
plt.tight_layout()
plt.show()
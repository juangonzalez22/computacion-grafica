import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def get_image_info(image):
    height, width = image.shape[:2]

    # Canales
    channels = 1 if image.ndim == 2 else image.shape[2]

    # Modo de color
    if channels == 1:
        color_mode = "Grayscale"
    elif channels == 3:
        color_mode = "RGB"
    elif channels == 4:
        color_mode = "RGBA"
    else:
        color_mode = f"{channels} channels (Unknown)"

    # Tipo de dato (Puede ser uint8, float32, etc.)
    dtype = image.dtype

    # Rango real
    min_val = float(image.min())
    max_val = float(image.max())
    actual_range = (min_val, max_val)

    # Detectar si parece normalizada
    is_normalized = (
        np.issubdtype(dtype, np.floating) and
        0.0 <= min_val and max_val <= 1.0
    )

    info = {
        "width": width, 
        "height": height,
        "channels": channels,
        "dtype": dtype,
        "color_mode": color_mode,
        "actual_range": actual_range,
        "is_normalized": is_normalized
    }

    return info

# 1. Extracción de canales RGB
def extract_rgb_channels(image):
    img_r = image.copy()
    img_g = image.copy()
    img_b = image.copy()
    
    img_r[:, :, 1] = img_r[:, :, 2] = 0
    img_g[:, :, 0] = img_g[:, :, 2] = 0
    img_b[:, :, 0] = img_b[:, :, 1] = 0
    return [img_r, img_g, img_b]

# 2. Extracción de canales CMYK
def extract_cymk_channels(image):
    img_c = image.copy()
    img_y = image.copy()
    img_m = image.copy()
    img_k = image.copy()
    
    img_c[:, :, 1] = img_c[:, :, 2] = 0
    img_y[:, :, 0] = img_y[:, :, 2] = 0
    img_m[:, :, 0] = img_m[:, :, 1] = 0
    img_k[:, :, :3] = 0
    return [img_c, img_y, img_m, img_k]

# 3. Inversión de colores
def invert_colors(image):
    img_inverted = image.copy()
    info = get_image_info(image)
    
    has_alpha = info["channels"] == 4
    rgb = img_inverted[:, :, :3] 
    
    if info["is_normalized"]:
        rgb = 1.0 - rgb
    else:
        rgb = 255 - rgb
    
    if has_alpha:
        img_inverted[:, :, :3] = rgb
    else:
        img_inverted = rgb
    return img_inverted

# 4. Conversión a monocromático
def monochrome(image):
    img_mono = image.copy()
    info = get_image_info(image)
    img_mono = 0.299 * img_mono[:, :, 0] + 0.587 * img_mono[:, :, 1] + 0.114 * img_mono[:, :, 2]
    return img_mono


def adjust_channel(image, channel, factor):

    info = get_image_info(image)
    img_adj = image.copy().astype(np.float32)
    max_val = 1.0 if info["is_normalized"] else 255.0
    
    offset = (factor / 100.0) * max_val
    channel = channel.upper()

    if channel == 'R':
        img_adj[:, :, 0] += offset
    elif channel == 'G':
        img_adj[:, :, 1] += offset
    elif channel == 'B':
        img_adj[:, :, 2] += offset
    
    elif channel == 'C':
        img_adj[:, :, 0] -= offset 
    elif channel == 'M':
        img_adj[:, :, 1] -= offset 
    elif channel == 'Y':
        img_adj[:, :, 2] -= offset 
        
    elif channel == 'K':
        img_adj[:, :, :3] -= offset


    img_adj[:, :, :3] = np.clip(img_adj[:, :, :3], 0, max_val)
    
    return img_adj.astype(info["dtype"])




# Prueba de las funciones
if __name__ == "__main__":
    # Cargar una imagen de ejemplo
    img_path = r"C:\Users\Admin\Desktop\computacion-grafica\Manejo de imagenes\images\gengar2.png"
    image = np.array(Image.open(img_path))

    # Obtener información de la imagen
    info = get_image_info(image)
    print("Información de la imagen:", info)
    
    # Brillo aumentado
    brighter_image = adjust_channel(image, "R", 100)
    plt.imshow(brighter_image)
    plt.title("Brillo Aumentado")
    plt.axis("off")
    plt.show()

    
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

# Función para asegurar que la imagen tenga 3 canales (RGB)
def ensure_3ch(image):
    if image.ndim == 2:
        image = np.stack([image]*3, axis=-1)
    return image

# 1. Extracción de canales RGB
def extract_rgb_channels(image):
    image = ensure_3ch(image)
    img_r = image.copy()
    img_g = image.copy()
    img_b = image.copy()
    
    img_r[:, :, 1] = img_r[:, :, 2] = 0
    img_g[:, :, 0] = img_g[:, :, 2] = 0
    img_b[:, :, 0] = img_b[:, :, 1] = 0
    return [img_r, img_g, img_b]

# 2. Extracción de canales CMYK (emulado en RGB)
def extract_cymk_channels(image):
    image = ensure_3ch(image)
    img_c = image.copy()
    img_m = image.copy()
    img_y = image.copy()
    img_k = image.copy()

    # Emulación simple: cada canal CMY reduce su canal complementario
    img_c[:, :, 0] = 0          # Cian "apaga" Rojo
    img_m[:, :, 1] = 0          # Magenta "apaga" Verde
    img_y[:, :, 2] = 0          # Amarillo "apaga" Azul
    img_k[:, :, :3] = 0         # Negro "apaga" todo

    return [img_c, img_m, img_y, img_k]
# 3. Inversión de colores
def invert_colors(image):
    img_inverted = image.copy()
    info = get_image_info(image)
    
    if info["channels"] == 1:
        if info["is_normalized"]:
            img_inverted = 1.0 - img_inverted
        else:
            img_inverted = 255 - img_inverted
        return img_inverted.astype(info["dtype"])

    rgb = img_inverted[:, :, :3]
    has_alpha = info["channels"] == 4
    
    if info["is_normalized"]:
        rgb = 1.0 - rgb
    else:
        rgb = 255 - rgb
    
    if has_alpha:
        img_inverted[:, :, :3] = rgb
    else:
        img_inverted = rgb
    return img_inverted.astype(info["dtype"])

# 4. Conversión a monocromático
def monochrome(image):
    image = ensure_3ch(image)
    img_mono = 0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]
    return img_mono

# 5. Ajuste de canal
def adjust_channel(image, channel, factor):
    info = get_image_info(image)
    img_adj = ensure_3ch(image).copy().astype(np.float32)
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
    else:
        raise ValueError("Canal desconocido, solo se permiten R,G,B,C,M,Y,K")

    img_adj[:, :, :3] = np.clip(img_adj[:, :, :3], 0, max_val)
    return img_adj.astype(info["dtype"])


# 6. Fusión de imágenes con ponderación (con 0 solo se ve la imagen B, con 1 solo se ve la imagen A)
def weighted_image_fusion(img_a_path, img_b_path, alpha=0.5):
    
    img_a = Image.open(img_a_path).convert("RGBA")
    img_b = Image.open(img_b_path).convert("RGBA")

    w, h = min(img_a.width, img_b.width), min(img_a.height, img_b.height)
    img_a = img_a.resize((w, h), Image.LANCZOS)
    img_b = img_b.resize((w, h), Image.LANCZOS)

    arr_a = np.array(img_a).astype(np.float32) / 255.0
    arr_b = np.array(img_b).astype(np.float32) / 255.0

    fusion = alpha * arr_a + (1 - alpha) * arr_b

    fusion = np.clip(fusion * 255, 0, 255).astype(np.uint8)
    return fusion


# 7. Ajuste de brillo (con value entre -1 y 1, donde 0 no cambia nada, -1 es completamente oscuro y 1 es completamente brillante)
def adjust_brightness(img, value):
    arr = img.astype(float)
    max_val = 255.0  # asumimos uint8
    if arr.ndim == 2:  # grayscale
        arr = arr + value*max_val
    elif arr.shape[2] in [3,4]:  # RGB o RGBA
        arr[:,:,:3] = arr[:,:,:3] + value*max_val
    arr = arr.clip(0, max_val)
    brighted = np.clip(arr, 0, max_val).astype(img.dtype)
    return brighted

# 8. Binarización (usando normalización de 0 a 1)
def binarize(image, threshold):
    has_alpha = (image.ndim == 3 and image.shape[2] == 4)
    if has_alpha:
        alpha = image[:,:,3].copy()
        rgb = image[:,:,:3]
    else:
        rgb = image

    img_gray = monochrome(rgb)
    img_bin = np.where(img_gray >= threshold, 1.0, 0.0)

    if has_alpha:
        img_bin = np.dstack([img_bin]*3 + [alpha])
    else:
        img_bin = np.stack([img_bin]*3, axis=-1) 

    return img_bin

# 9. Traslación de imagen (dx, dy pueden ser positivos o negativos, con relleno de fondo)
def translate_image(image, dx, dy):

    h, w = image.shape[:2]
    
    if image.ndim == 3 and image.shape[2] == 4:
        translated = np.zeros_like(image)
    else:
        translated = np.zeros_like(image) 

    x1d = max(0, dx)
    y1d = max(0, dy)
    x2d = min(w, w+dx)
    y2d = min(h, h+dy)

    x1s = max(0, -dx)
    y1s = max(0, -dy)
    x2s = x1s + (x2d - x1d)
    y2s = y1s + (y2d - y1d)

    if x2d > x1d and y2d > y1d:
        translated[y1d:y2d, x1d:x2d] = image[y1s:y2s, x1s:x2s]

    return translated


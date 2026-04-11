import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2


def get_image_info(image):
    shape = image.shape
    ndim = image.ndim
    height, width = shape[:2]
    channels = 1 if ndim == 2 else shape[2]
    is_grayscale = (channels == 1)
    has_alpha = (channels == 4)

    if is_grayscale:
        color_mode = "Grayscale"
    elif channels == 3:
        color_mode = "RGB"
    elif has_alpha:
        color_mode = "RGBA"
    else:
        color_mode = f"{channels} channels (Unknown)"
        
    dtype = image.dtype

    min_val = float(image.min())
    max_val = float(image.max())
    actual_range = (min_val, max_val)

    is_normalized = (
        np.issubdtype(dtype, np.floating) and
        0.0 <= min_val and max_val <= 1.0
    )

    theoretical_max = 1.0 if is_normalized else 255.0

    info = {
        "shape": shape,
        "ndim": ndim,
        "width": width, 
        "height": height,
        "aspect_ratio": width / height if height > 0 else 0,
        "channels": channels,
        "is_grayscale": is_grayscale,
        "has_alpha": has_alpha,
        "dtype": dtype,
        "color_mode": color_mode,
        "actual_range": actual_range,
        "is_normalized": is_normalized,
        "theoretical_max": theoretical_max
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
    img_c[:, :, 0] = 0  
    img_m[:, :, 1] = 0  
    img_y[:, :, 2] = 0 
    img_k[:, :, :3] = 0

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
    if image.ndim == 2:
        return image
        
    img_mono = 0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]
    
    if image.shape[2] == 4:
        alpha = image[:, :, 3]
        return np.dstack([img_mono]*3 + [alpha]).astype(image.dtype)
        
    return img_mono.astype(image.dtype)

# 5. Ajuste de canal
def adjust_channel(image, channel, factor):
    info = get_image_info(image)
    img_adj = ensure_3ch(image).copy().astype(np.float32)
    
    max_val = info["theoretical_max"]
    
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
def weighted_image_fusion(img_a, img_b, alpha=0.5):

    # Asegurar mismo tamaño
    h = min(img_a.shape[0], img_b.shape[0])
    w = min(img_a.shape[1], img_b.shape[1])

    img_a = np.array(Image.fromarray(img_a).resize((w, h), Image.LANCZOS))
    img_b = np.array(Image.fromarray(img_b).resize((w, h), Image.LANCZOS))

    arr_a = img_a.astype(np.float32) / 255.0
    arr_b = img_b.astype(np.float32) / 255.0

    fusion = alpha * arr_a + (1 - alpha) * arr_b

    return np.clip(fusion * 255, 0, 255).astype(np.uint8)


# 7. Ajuste de brillo (con value entre -1 y 1, donde 0 no cambia nada, -1 es completamente oscuro y 1 es completamente brillante)
def adjust_brightness(img, value):
    info = get_image_info(img)
    arr = img.astype(float)
    max_val = info["theoretical_max"] 
    
    if info["is_grayscale"]:
        arr = arr + value * max_val
    else:
        arr[:, :, :3] = arr[:, :, :3] + value * max_val
        
    brighted = np.clip(arr, 0, max_val).astype(info["dtype"])
    
    return brighted

# 8. Binarización (usando normalización de 0 a 1)
def binarize(image, threshold):
    info = get_image_info(image)
    has_alpha = info["has_alpha"]
    max_val = info["theoretical_max"]
    
    if has_alpha:
        alpha = image[:,:,3].copy()
        rgb = image[:,:,:3]
    else:
        rgb = image

    img_gray = monochrome(rgb)
    
    img_bin = np.where(img_gray >= threshold, max_val, 0).astype(info["dtype"])

    if has_alpha:
        img_bin = np.dstack([img_bin]*3 + [alpha])
    else:
        img_bin = np.stack([img_bin]*3, axis=-1) 

    return img_bin

# 9. Traslación de imagen (dx, dy pueden ser positivos o negativos, con relleno de fondo)
def translate_image(image, dx, dy):
    h, w = image.shape[:2]
    
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
# 10. Recorte
def cut(image, x1, x2, y1, y2):
    h, w = image.shape[:2]
    x1 = max(0, x1)
    x2 = min(w, x2)
    y1 = max(0, y1)
    y2 = min(h, y2)
    return image[y1:y2, x1:x2]

# 11. Zoom
def zoom(image, factor):
    info = get_image_info(image)
    h, w = info["height"], info["width"]
    if info["is_grayscale"]:
        pil_mode = "L"
    elif info["has_alpha"]:
        pil_mode = "RGBA"
    else:
        pil_mode = "RGB"

    if factor > 1:
        new_h = int(h / factor)
        new_w = int(w / factor)
        y1 = (h - new_h) // 2
        y2 = y1 + new_h
        x1 = (w - new_w) // 2
        x2 = x1 + new_w
        
        # Recorte
        if info["is_grayscale"]:
            img_crop = image[y1:y2, x1:x2]
        else:
            img_crop = image[y1:y2, x1:x2, :]
    else:
        new_h = max(1, int(h * factor))
        new_w = max(1, int(w * factor))
        
        img_crop = np.array(Image.fromarray(image, mode=pil_mode).resize((new_w, new_h), Image.LANCZOS))

        canvas = np.zeros_like(image)
        y_offset = (h - new_h) // 2
        x_offset = (w - new_w) // 2
        
        if info["is_grayscale"]:
            canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = img_crop
        else:
            canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w, :] = img_crop
            
        img_crop = canvas

    if factor > 1:
        img_crop = np.array(Image.fromarray(img_crop, mode=pil_mode).resize((w, h), Image.LANCZOS))

    return img_crop

# 12. Reducción de resolución (factor entre 1 y 0. 1 no cambia nada y 0 es pixelado extremo)
def reduce_resolution(image, factor):
    factor = max(0.001, factor)
    step = max(1, int(1/factor))
    return image[::step, ::step]

# 13. Detección de bordes Canny
def canny_edge_detection(image, threshold1=100, threshold2=200):
    info = get_image_info(image)
    
    if info["has_alpha"]:
        alpha = image[:, :, 3]
        rgb = image[:, :, :3]
    else:
        rgb = image
        
    gray = rgb if info["is_grayscale"] else monochrome(rgb)
    
    if info["is_normalized"]:
        gray = gray * 255.0
        
    edges = cv2.Canny(gray.astype(np.uint8), threshold1, threshold2)
    
    if info["has_alpha"]:
        edges = np.dstack([edges]*3 + [alpha])
        
    return edges
    
# 14. Detección de bordes Sobel
def sobel_edge_detection(image, threshold=100):
    info = get_image_info(image)
    
    if info["has_alpha"]:
        alpha = image[:, :, 3]
        rgb = image[:, :, :3]
    else:
        rgb = image

    if not info["is_grayscale"]:
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    else:
        gray = rgb
    
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    
    sobel_mag = np.sqrt(sobelx**2 + sobely**2)
    sobel_mag = cv2.normalize(sobel_mag, None, 0, 255, cv2.NORM_MINMAX)
    
    edges = np.where(sobel_mag > threshold, 255.0, 0.0).astype(np.uint8)
    
    if info["has_alpha"]:
        edges = np.dstack([edges]*3 + [alpha])
        
    return edges

# 15. Segmentación por color en espacio HSV
def segment_hsv(image, lower_hsv, upper_hsv, return_mask=True, return_segmented=True):
    info = get_image_info(image)
    
    if info["is_grayscale"]:
        raise ValueError("No se puede segmentar en HSV una imagen en escala de grises.")
    
    if info["has_alpha"]:
        rgb_image = image[:, :, :3]
    else:
        rgb_image = image.copy()
        
    if info["is_normalized"]:
        rgb_image = (rgb_image * 255.0).astype(np.uint8)
    elif info["dtype"] != np.uint8:
        rgb_image = rgb_image.astype(np.uint8)
        
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)

    mask = cv2.inRange(hsv, np.array(lower_hsv), np.array(upper_hsv))
    
    segmented = cv2.bitwise_and(image, image, mask=mask)

    results = []
    if return_mask:
        results.append(mask)
    if return_segmented:
        results.append(segmented)

    if len(results) == 1:
        return results[0]
    return tuple(results)

# 16. Rotación
def rotate_image(image, angle_deg, background=0):
    info = get_image_info(image)
    
    ang = np.deg2rad(angle_deg)
    cos_t, sin_t = np.cos(ang), np.sin(ang)

    h, w = info["height"], info["width"]
    has_alpha = info["has_alpha"]
    is_gray = info["is_grayscale"]

    cx, cy = (w - 1) / 2.0, (h - 1) / 2.0

    corners = np.array([
        [0, 0],
        [w-1, 0],
        [w-1, h-1],
        [0, h-1]
    ], dtype=np.float32)

    x = corners[:, 0] - cx
    y = corners[:, 1] - cy

    xr = x * cos_t - y * sin_t
    yr = x * sin_t + y * cos_t

    min_x, max_x = xr.min(), xr.max()
    min_y, max_y = yr.min(), yr.max()

    out_w = int(np.ceil(max_x - min_x + 1))
    out_h = int(np.ceil(max_y - min_y + 1))

    out_cx, out_cy = (out_w - 1) / 2.0, (out_h - 1) / 2.0

    if is_gray:
        out = np.full((out_h, out_w), background, dtype=image.dtype)
    else:
        channels = image.shape[2]
        out = np.full((out_h, out_w, channels), background, dtype=image.dtype)

    for y_out in range(out_h):
        for x_out in range(out_w):

            x2 = x_out - out_cx
            y2 = y_out - out_cy

            x1 = x2 * cos_t + y2 * sin_t
            y1 = -x2 * sin_t + y2 * cos_t

            x_src = x1 + cx
            y_src = y1 + cy

            xi = int(round(x_src))
            yi = int(round(y_src))

            if 0 <= xi < w and 0 <= yi < h:
                out[y_out, x_out] = image[yi, xi]

    return out

def rotate_fast(image, angle_deg, background=0):
    info = get_image_info(image)

    h, w = info["height"], info["width"]
    has_alpha = info["has_alpha"]
    is_gray = info["is_grayscale"]

    cx, cy = w / 2.0, h / 2.0

    # Matriz de rotación
    M = cv2.getRotationMatrix2D((cx, cy), angle_deg, 1.0)

    cos = abs(M[0, 0])
    sin = abs(M[0, 1])

    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    M[0, 2] += (new_w / 2) - cx
    M[1, 2] += (new_h / 2) - cy

    if is_gray:
        border_value = background
    else:
        channels = image.shape[2]
        if isinstance(background, (list, tuple, np.ndarray)):
            border_value = background
        else:
            border_value = [background] * channels

    rotated = cv2.warpAffine(
        image,
        M,
        (new_w, new_h),
        flags=cv2.INTER_NEAREST,  # mismo estilo que tu versión manual
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border_value
    )

    return rotated


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



if __name__ == "__main__":
    import os
    import sys

    print("--- Batería de Pruebas de Procesamiento de Imágenes ---")
    img_jpg_path = input("Ingresa la ruta de la imagen JPG").strip()
    img_png_path = input("Ingresa la ruta de la imagen PNG").strip()

    if not os.path.exists(img_jpg_path) or not os.path.exists(img_png_path):
        print("Error: Una o ambas rutas no existen. Verifica y vuelve a intentar.")
        sys.exit(1)

    img_jpg = np.array(Image.open(img_jpg_path).convert("RGB"))
    
    img_png_pil = Image.open(img_png_path)
    if img_png_pil.mode in ('RGBA', 'LA') or (img_png_pil.mode == 'P' and 'transparency' in img_png_pil.info):
        img_png = np.array(img_png_pil.convert("RGBA"))
    else:
        img_png = np.array(img_png_pil.convert("RGB"))

    images_to_test = [
        ("JPG", img_jpg),
        ("PNG", img_png)
    ]

    plots = []

    lower_red = [150, 50, 50]
    upper_red = [180, 255, 255]

    for format_name, img in images_to_test:
        plots.append((f"Original {format_name}", img, None))

        rgb_ch = extract_rgb_channels(img)
        plots.append((f"Red Ch {format_name}", rgb_ch[0], None))
        plots.append((f"Green Ch {format_name}", rgb_ch[1], None))
        plots.append((f"Blue Ch {format_name}", rgb_ch[2], None))

        cmyk_ch = extract_cymk_channels(img)
        plots.append((f"Cyan Ch {format_name}", cmyk_ch[0], None))
        plots.append((f"Magenta Ch {format_name}", cmyk_ch[1], None))
        plots.append((f"Yellow Ch {format_name}", cmyk_ch[2], None))
        plots.append((f"Key (Blk) Ch {format_name}", cmyk_ch[3], None))

        plots.append((f"Invert {format_name}", invert_colors(img), None))
        plots.append((f"Monochrome {format_name}", monochrome(img), 'gray'))
        
        plots.append((f"Adj Channel R+50% {format_name}", adjust_channel(img, 'R', 50), None))
        plots.append((f"Adj Brightness +0.3 {format_name}", adjust_brightness(img, 0.3), None))
        
        plots.append((f"Binarize {format_name}", binarize(img, 128), 'gray'))

        plots.append((f"Translate dx50 dy50 {format_name}", translate_image(img, 50, 50), None))
        
        h, w = img.shape[:2]
        cx, cy = w//2, h//2
        plots.append((f"Cut Center {format_name}", cut(img, cx-50, cx+50, cy-50, cy+50), None))
        
        plots.append((f"Zoom IN 2.0x {format_name}", zoom(img, 2.0), None))
        plots.append((f"Zoom OUT 0.5x {format_name}", zoom(img, 0.5), None))
        plots.append((f"Reduce Res 0.1x {format_name}", reduce_resolution(img, 0.1), None))

        plots.append((f"Canny {format_name}", canny_edge_detection(img), 'gray'))
        plots.append((f"Sobel {format_name}", sobel_edge_detection(img), 'gray'))

        try:
            mask, seg = segment_hsv(img, lower_red, upper_red)
            plots.append((f"HSV Mask {format_name}", mask, 'gray'))
            plots.append((f"HSV Segmented {format_name}", seg, None))
        except Exception as e:
            plots.append((f"HSV Error {format_name}", np.zeros((10,10)), 'gray'))


    fusion_img = weighted_image_fusion(img_jpg_path, img_png_path, alpha=0.5)
    plots.append(("Fusión (Alpha 0.5)", fusion_img, None))

    rows, cols = 6, 8
    fig, axes = plt.subplots(rows, cols, figsize=(24, 16))
    fig.canvas.manager.set_window_title('Resultados de Procesamiento de Imágenes')
    
    axes = axes.flatten()
    for i, (title, img_data, cmap) in enumerate(plots):
        ax = axes[i]
        
        if img_data.dtype == np.float32 or img_data.dtype == np.float64:
            if img_data.max() > 1.0:
                 img_data = img_data / 255.0
                 
        ax.imshow(img_data, cmap=cmap)
        ax.set_title(title, fontsize=8)
        ax.axis('off')

    for j in range(len(plots), len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()
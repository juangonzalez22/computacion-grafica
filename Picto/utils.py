from PIL import Image


def image_to_pil(img):
    if img.ndim == 2:
        return Image.fromarray(img)
    if img.shape[2] == 4:
        return Image.fromarray(img, "RGBA")
    return Image.fromarray(img[:, :, :3], "RGB")
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Leer imagen en gris
img = cv2.imread("letras.jpg", 0)

# ---------------------------
# 1) Roberts (2x2)
# ---------------------------
k_roberts_x = np.array([[1, 0],
                        [0,-1]], dtype=np.float32)
k_roberts_y = np.array([[0, 1],
                        [-1,0]], dtype=np.float32)

roberts_x = cv2.filter2D(img, cv2.CV_64F, k_roberts_x)
roberts_y = cv2.filter2D(img, cv2.CV_64F, k_roberts_y)
roberts = np.sqrt(roberts_x**2 + roberts_y**2)
roberts = cv2.normalize(roberts, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# ---------------------------
# 2) Sobel X y Y
# ---------------------------
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
sobel_mag = np.sqrt(sobelx**2 + sobely**2)
sobel_mag = cv2.normalize(sobel_mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

sobelx_u8 = cv2.normalize(np.abs(sobelx), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
sobely_u8 = cv2.normalize(np.abs(sobely), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# ---------------------------
# 3) Prewitt (3x3)
# ---------------------------
k_prewitt_x = np.array([[-1, 0, 1],
                        [-1, 0, 1],
                        [-1, 0, 1]], dtype=np.float32)
k_prewitt_y = np.array([[ 1, 1, 1],
                        [ 0, 0, 0],
                        [-1,-1,-1]], dtype=np.float32)

prewitt_x = cv2.filter2D(img, cv2.CV_64F, k_prewitt_x)
prewitt_y = cv2.filter2D(img, cv2.CV_64F, k_prewitt_y)
prewitt = np.sqrt(prewitt_x**2 + prewitt_y**2)
prewitt = cv2.normalize(prewitt, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# ---------------------------
# 4) Laplaciano
# ---------------------------
lap = cv2.Laplacian(img, cv2.CV_64F, ksize=3)
lap = cv2.normalize(np.abs(lap), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# ---------------------------
# 5) Canny
# ---------------------------
canny = cv2.Canny(img, 80, 160)

# ---------------------------
# Mostrar resultados
# ---------------------------
plt.figure(figsize=(12, 8))

plt.subplot(2,4,1); plt.imshow(img, cmap="gray");       plt.title("Original"); plt.axis("off")
plt.subplot(2,4,2); plt.imshow(roberts, cmap="gray");   plt.title("Roberts");  plt.axis("off")
plt.subplot(2,4,3); plt.imshow(sobelx_u8, cmap="gray"); plt.title("Sobel X");  plt.axis("off")
plt.subplot(2,4,4); plt.imshow(sobely_u8, cmap="gray"); plt.title("Sobel Y");  plt.axis("off")

plt.subplot(2,4,5); plt.imshow(sobel_mag, cmap="gray"); plt.title("Sobel Mag"); plt.axis("off")
plt.subplot(2,4,6); plt.imshow(prewitt, cmap="gray");   plt.title("Prewitt");   plt.axis("off")
plt.subplot(2,4,7); plt.imshow(lap, cmap="gray");       plt.title("Laplaciano");plt.axis("off")
plt.subplot(2,4,8); plt.imshow(canny, cmap="gray");     plt.title("Canny");     plt.axis("off")

plt.tight_layout()
plt.show()
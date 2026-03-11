import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("asegmentar.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_color_a = np.array([100, 80, 40])
upper_color_a = np.array([140, 255, 255])

lower_color_b = np.array([40, 60, 50])
upper_color_b = np.array([85, 255, 255])

lower_color_c = np.array([0, 70, 50])
upper_color_c = np.array([15, 255, 255])


mask_a = cv2.inRange(hsv, lower_color_a, upper_color_a)
mask_b = cv2.inRange(hsv, lower_color_b, upper_color_b)
mask_c1 = cv2.inRange(hsv, np.array([0, 70, 50]), np.array([10, 255, 255]))
mask_c2 = cv2.inRange(hsv, np.array([170, 70, 50]), np.array([180, 255, 255]))
mask_c = cv2.bitwise_or(mask_c1, mask_c2)

seg_a = cv2.bitwise_and(img, img, mask=mask_a)
seg_b = cv2.bitwise_and(img, img, mask=mask_b)
seg_c = cv2.bitwise_and(img, img, mask=mask_c)

segmentation = cv2.bitwise_or(seg_a, cv2.bitwise_or(seg_b, seg_c))

plt.figure(figsize=(15,4))

plt.subplot(1,5,1); plt.title("Original"); plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); plt.axis("off")
plt.subplot(1,5,2); plt.title("Máscara azul"); plt.imshow(cv2.cvtColor(seg_a, cv2.COLOR_BGR2RGB)); plt.axis("off")
plt.subplot(1,5,3); plt.title("Máscara verde"); plt.imshow(cv2.cvtColor(seg_b, cv2.COLOR_BGR2RGB)); plt.axis("off")
plt.subplot(1,5,4); plt.title("Máscara roja"); plt.imshow(cv2.cvtColor(seg_c, cv2.COLOR_BGR2RGB)); plt.axis("off")
plt.subplot(1,5,5); plt.title("Segmentación completa"); plt.imshow(cv2.cvtColor(segmentation, cv2.COLOR_BGR2RGB)); plt.axis("off")

plt.tight_layout()
plt.show()
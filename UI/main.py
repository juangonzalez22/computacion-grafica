import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

from imagelib import adjust_brightness

image = None
original_image = None


def open_image():
    global image, original_image

    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )

    if file_path:
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

        if image is None:
            messagebox.showerror("Error", "Could not load image")
            return

        original_image = image.copy()

        slider.set(0)
        entry.delete(0, tk.END)
        entry.insert(0, "0")

        display_image()


def display_image():
    if image is None:
        return

    if len(image.shape) == 3:
        img_rgb = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2RGB)
    else:
        img_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    img_pil = Image.fromarray(img_rgb)
    max_width, max_height = 400, 300

    w, h = img_pil.size
    scale = min(max_width / w, max_height / h)

    new_size = (int(w * scale), int(h * scale))
    img_pil = img_pil.resize(new_size)

    img_tk = ImageTk.PhotoImage(img_pil)

    image_label.config(image=img_tk)
    image_label.image = img_tk


def apply_from_entry():
    global image, original_image

    if original_image is None:
        messagebox.showwarning("Warning", "Open an image first")
        return
    try:
        value = float(entry.get())
        value = max(-1, min(1, value))

        image = adjust_brightness(original_image.copy(), int(value * 100))

        original_image = image.copy()

        # reset UI
        slider.set(0)
        entry.delete(0, tk.END)
        entry.insert(0, "0")

        display_image()

    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")




def reset_image():
    global image

    if original_image is None:
        return

    image = original_image.copy()

    slider.set(0)
    entry.delete(0, tk.END)
    entry.insert(0, "0")

    display_image()
    
    
def update_entry(value):
    entry.delete(0, tk.END)
    entry.insert(0, f"{float(value):.2f}")

# UI
window = tk.Tk()
window.title("Image Brightness")
window.geometry("520x500")

open_button = tk.Button(window, text="Open Image", command=open_image)
open_button.pack(pady=10)

entry = tk.Entry(window, width=10)
entry.pack()
entry.insert(0, "0")

apply_button = tk.Button(window, text="Apply Brightness", command=apply_from_entry)
apply_button.pack(pady=5)

reset_button = tk.Button(window, text="Reset", command=reset_image)
reset_button.pack(pady=5)

slider = tk.Scale(
    window,
    from_=-1,
    resolution=0.01,
    to=1,
    orient="horizontal",
    length=200,
    label="Brightness",
    command=update_entry
)
slider.pack(pady=10)

image_label = tk.Label(window)
image_label.pack(pady=10)

window.mainloop()
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import imagelib as imglib

first_image = None     # original
base_image = None      # brillo aplicado
current_image = None   # lo que se muestra


# ---------------- IMAGE ----------------

def open_image():
    global first_image, base_image

    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )

    if not file_path:
        return

    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        messagebox.showerror("Error", "Could not load image")
        return

    first_image = img.copy()
    base_image = img.copy()

    display_with_channels()


def display_image(img):
    if len(img.shape) == 3:
        img_rgb = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2RGB)
    else:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    img_pil = Image.fromarray(img_rgb)

    max_w, max_h = 400, 300
    w, h = img_pil.size
    scale = min(max_w / w, max_h / h)

    img_pil = img_pil.resize((int(w * scale), int(h * scale)))

    img_tk = ImageTk.PhotoImage(img_pil)

    image_label.config(image=img_tk)
    image_label.image = img_tk


def display_with_channels():
    global current_image

    if base_image is None:
        return

    r, g, b = imglib.extract_rgb_channels(base_image)

    img = None

    if var_r.get():
        img = r.copy() if img is None else img + r
    if var_g.get():
        img = g.copy() if img is None else img + g
    if var_b.get():
        img = b.copy() if img is None else img + b

    if img is None:
        img = base_image.copy()
        img[:] = 0

    current_image = img
    display_image(current_image)


# ---------------- BRIGHTNESS ----------------

def apply_brightness():
    global base_image

    if first_image is None:
        return

    value = float(brightness_slider.get())
    
    base_image = imglib.adjust_brightness(first_image.copy(), value)

    display_with_channels()


# ---------------- RESET ----------------

def reset_all():
    global base_image

    if first_image is None:
        return

    base_image = first_image.copy()
    brightness_slider.set(0)

    var_r.set(True)
    var_g.set(True)
    var_b.set(True)

    display_with_channels()


# ---------------- UI ----------------

window = tk.Tk()
window.title("Image Editor")
window.geometry("500x500")

image_label = tk.Label(window)
image_label.pack(pady=20)

tk.Button(window, text="Open Image", command=open_image).pack(pady=10)

controls = tk.Frame(window)
controls.pack(pady=10)

brightness_slider = tk.Scale(
    controls,
    from_=-1,
    to=1,
    resolution=0.01,
    orient="horizontal",
    length=200,
    label="Brightness"
)
brightness_slider.grid(row=0, column=0)

tk.Button(controls, text="Apply", command=apply_brightness).grid(row=0, column=1, padx=5)

var_r = tk.BooleanVar(value=True)
var_g = tk.BooleanVar(value=True)
var_b = tk.BooleanVar(value=True)

tk.Checkbutton(window, text="Red", variable=var_r, command=display_with_channels).pack()
tk.Checkbutton(window, text="Green", variable=var_g, command=display_with_channels).pack()
tk.Checkbutton(window, text="Blue", variable=var_b, command=display_with_channels).pack()

tk.Button(window, text="Reset", command=reset_all).pack(pady=10)

window.mainloop()
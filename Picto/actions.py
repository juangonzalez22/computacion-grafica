import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

import state
import controls as ctrl
import imagelib as imglib
from constants import (
    DEFAULT_BRIGHTNESS, DEFAULT_CHANNEL_R, DEFAULT_CHANNEL_G, DEFAULT_CHANNEL_B,
    DEFAULT_TRANSLATION_X, DEFAULT_TRANSLATION_Y, DEFAULT_ROTATION,
    DEFAULT_BINARIZE_THRESHOLD, DEFAULT_RESOLUTION_SCALE, DEFAULT_ALPHA,
    DEFALUT_LOWER_H, DEFALUT_LOWER_S, DEFALUT_LOWER_V,
    DEFALUT_UPPER_H, DEFALUT_UPPER_S, DEFALUT_UPPER_V,
    DEFAULT_CANNY_TH1, DEFAULT_CANNY_TH2, DEFAULT_SOBEL_TH, DEFAULT_ZOOM,
    DEFAULT_ENABLED_RGB, DEFAULT_ENABLED_R, DEFAULT_ENABLED_G, DEFAULT_ENABLED_B,
    DEFAULT_ENABLED_NEGATIVE, DEFAULT_ENABLED_MONOCHROME,
    DEFAULT_ENABLE_BINARIZE, DEFAULT_ENABLE_FUSION,
    DEFAULT_ENABLE_CANNY, DEFAULT_ENABLE_SOBEL,
)
from utils import image_to_pil


def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if not file_path:
        return

    state.image_path = file_path

    img_pil = Image.open(file_path)

    if img_pil.mode in ("RGBA", "LA") or ("transparency" in img_pil.info):
        img_pil = img_pil.convert("RGBA")
    else:
        img_pil = img_pil.convert("RGB")

    img = np.array(img_pil)

    state.first_image = state.current_image = state.preview_image = img.copy()

    h, w = img.shape[:2]

    ctrl.x_translation_slider.config(from_=-w, to=w)
    ctrl.y_translation_slider.config(from_=-h, to=h)
    ctrl.width_slider.config(from_=1, to=w)
    ctrl.height_slider.config(from_=1, to=h)

    ctrl.width_slider.set(w)
    ctrl.height_slider.set(h)

    ctrl.rgb_enabled.set(DEFAULT_ENABLED_RGB)
    ctrl.canny_enabled.set(DEFAULT_ENABLE_CANNY)
    ctrl.sobel_enabled.set(DEFAULT_ENABLE_SOBEL)
    ctrl.negative_enabled.set(DEFAULT_ENABLED_NEGATIVE)
    ctrl.monochrome_enabled.set(DEFAULT_ENABLED_MONOCHROME)
    ctrl.binarize_enabled.set(DEFAULT_ENABLE_BINARIZE)
    ctrl.fusion_enabled.set(DEFAULT_ENABLE_FUSION)

    ctrl.canny_th1_slider.set(DEFAULT_CANNY_TH1)
    ctrl.canny_th2_slider.set(DEFAULT_CANNY_TH2)
    ctrl.sobel_th_slider.set(DEFAULT_SOBEL_TH)
    ctrl.rotation_slider.set(DEFAULT_ROTATION)
    ctrl.brightness_slider.set(DEFAULT_BRIGHTNESS)
    ctrl.red_slider.set(DEFAULT_CHANNEL_R)
    ctrl.green_slider.set(DEFAULT_CHANNEL_G)
    ctrl.blue_slider.set(DEFAULT_CHANNEL_B)
    ctrl.x_translation_slider.set(DEFAULT_TRANSLATION_X)
    ctrl.y_translation_slider.set(DEFAULT_TRANSLATION_Y)
    ctrl.zoom_slider.set(DEFAULT_ZOOM)
    ctrl.resolution_slider.set(DEFAULT_RESOLUTION_SCALE)
    ctrl.alpha_slider.set(DEFAULT_ALPHA)

    ctrl.var_r.set(DEFAULT_ENABLED_R)
    ctrl.var_g.set(DEFAULT_ENABLED_G)
    ctrl.var_b.set(DEFAULT_ENABLED_B)

    ctrl.h_min.set(DEFALUT_LOWER_H)
    ctrl.s_min.set(DEFALUT_LOWER_S)
    ctrl.v_min.set(DEFALUT_LOWER_V)
    ctrl.h_max.set(DEFALUT_UPPER_H)
    ctrl.s_max.set(DEFALUT_UPPER_S)
    ctrl.v_max.set(DEFALUT_UPPER_V)

    update_preview()


def save_image():
    if state.preview_image is None:
        messagebox.showwarning("WARNING!", "There is no image to save. Please open an image first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg;*.jpeg"),
            ("Bitmap", "*.bmp"),
            ("All Files", "*.*")
        ],
        title="Save Image As..."
    )
    if not file_path:
        return

    try:
        img_to_save = image_to_pil(state.preview_image)
        img_to_save.save(file_path)
        messagebox.showinfo("SUCCESS!", f"Image saved successfully in:\n{file_path}")
    except Exception as e:
        messagebox.showerror("ERROR!", f"An error occurred while saving the image:\n{str(e)}")


def display_image(img):
    from PIL import ImageTk

    if img is None:
        return

    img_pil = image_to_pil(img)

    cont_w = ctrl.left_container.winfo_width()
    cont_h = ctrl.left_container.winfo_height()

    if cont_w <= 1 or cont_h <= 1:
        cont_w, cont_h = 500, 400

    max_w = cont_w - 10
    max_h = cont_h - 10

    w, h = img_pil.size
    if w == 0 or h == 0:
        return

    scale = min(max_w / w, max_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    img_pil = img_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)

    img_tk = ImageTk.PhotoImage(img_pil)
    ctrl.image_label.config(image=img_tk)
    ctrl.image_label.image = img_tk


def update_preview(event=None):
    if state.current_image is None:
        return

    img = state.current_image.copy()

    if ctrl.rgb_enabled.get():
        r, g, b = imglib.extract_rgb_channels(img)
        channels = []
        if ctrl.var_r.get():
            channels.append(r)
        if ctrl.var_g.get():
            channels.append(g)
        if ctrl.var_b.get():
            channels.append(b)

        if channels:
            img = np.zeros_like(img)
            for ch in channels:
                img = img + ch
        else:
            img[:] = 0

    r_val = ctrl.red_slider.get()
    g_val = ctrl.green_slider.get()
    b_val = ctrl.blue_slider.get()

    if r_val != 0:
        img = imglib.adjust_channel(img, 'R', r_val)
    if g_val != 0:
        img = imglib.adjust_channel(img, 'G', g_val)
    if b_val != 0:
        img = imglib.adjust_channel(img, 'B', b_val)

    if ctrl.monochrome_enabled.get():
        img = imglib.monochrome(img)

    img = imglib.adjust_brightness(img, float(ctrl.brightness_slider.get()))

    if ctrl.negative_enabled.get():
        img = imglib.invert_colors(img)

    if ctrl.binarize_enabled.get():
        img = imglib.binarize(img, ctrl.binarize_slider.get())

    img = imglib.translate_image(
        img,
        int(ctrl.x_translation_slider.get()),
        int(ctrl.y_translation_slider.get())
    )

    if ctrl.cut_enabled.get():
        w = min(int(ctrl.width_slider.get()), img.shape[1])
        h = min(int(ctrl.height_slider.get()), img.shape[0])
        img = imglib.cut(img, 0, w, 0, h)

    img = imglib.zoom(img, 2 ** float(ctrl.zoom_slider.get()))
    img = imglib.reduce_resolution(img, float(ctrl.resolution_slider.get()))

    if ctrl.hsv_enabled.get():
        lower = (ctrl.h_min.get(), ctrl.s_min.get(), ctrl.v_min.get())
        upper = (ctrl.h_max.get(), ctrl.s_max.get(), ctrl.v_max.get())
        _, img = imglib.segment_hsv(img, lower, upper)

    if ctrl.canny_enabled.get():
        img = imglib.canny_edge_detection(img, ctrl.canny_th1_slider.get(), ctrl.canny_th2_slider.get())

    if ctrl.sobel_enabled.get():
        img = imglib.sobel_edge_detection(img, ctrl.sobel_th_slider.get())

    if ctrl.rotation_slider.get() != 0:
        img = imglib.rotate_fast(img, ctrl.rotation_slider.get())

    if ctrl.fusion_enabled.get() and state.second_image is not None:
        img = imglib.weighted_image_fusion(img, state.second_image, float(ctrl.alpha_slider.get()))

    state.preview_image = img
    display_image(img)


def apply_changes():
    if state.preview_image is None:
        return

    state.current_image = state.preview_image.copy()
    reset_preview()

    h, w = state.current_image.shape[:2]
    ctrl.width_slider.config(from_=1, to=w)
    ctrl.height_slider.config(from_=1, to=h)
    ctrl.x_translation_slider.config(from_=-w, to=w)
    ctrl.y_translation_slider.config(from_=-h, to=h)


def reset_preview():
    ctrl.brightness_slider.set(DEFAULT_BRIGHTNESS)
    ctrl.rgb_enabled.set(False)
    ctrl.var_r.set(True)
    ctrl.var_g.set(True)
    ctrl.var_b.set(True)
    ctrl.negative_enabled.set(False)
    ctrl.monochrome_enabled.set(False)
    ctrl.binarize_enabled.set(False)

    ctrl.red_slider.set(DEFAULT_CHANNEL_R)
    ctrl.green_slider.set(DEFAULT_CHANNEL_G)
    ctrl.blue_slider.set(DEFAULT_CHANNEL_B)
    ctrl.x_translation_slider.set(DEFAULT_TRANSLATION_X)
    ctrl.y_translation_slider.set(DEFAULT_TRANSLATION_Y)
    ctrl.width_slider.set(ctrl.width_slider.cget("to"))
    ctrl.height_slider.set(ctrl.height_slider.cget("to"))
    ctrl.zoom_slider.set(DEFAULT_ZOOM)
    ctrl.resolution_slider.set(DEFAULT_RESOLUTION_SCALE)

    ctrl.canny_enabled.set(False)
    ctrl.sobel_enabled.set(False)
    ctrl.rotation_slider.set(DEFAULT_ROTATION)
    ctrl.h_min.set(DEFALUT_LOWER_H)
    ctrl.s_min.set(DEFALUT_LOWER_S)
    ctrl.v_min.set(DEFALUT_LOWER_V)
    ctrl.h_max.set(DEFALUT_UPPER_H)
    ctrl.s_max.set(DEFALUT_UPPER_S)
    ctrl.v_max.set(DEFALUT_UPPER_V)

    ctrl.fusion_enabled.set(False)
    ctrl.alpha_slider.set(DEFAULT_ALPHA)
    ctrl.canny_th1_slider.set(DEFAULT_CANNY_TH1)
    ctrl.canny_th2_slider.set(DEFAULT_CANNY_TH2)
    ctrl.sobel_th_slider.set(DEFAULT_SOBEL_TH)

    update_preview()


def load_second_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if not file_path:
        return

    img = Image.open(file_path).convert("RGB")
    state.second_image = np.array(img)


def show_image_info():
    if state.preview_image is None:
        messagebox.showwarning("WARNING!", "No image is loaded.")
        return

    info_win = tk.Toplevel()
    info_win.title("Image Info")
    info_win.geometry("800x600")
    info_win.configure(bg="#2b2b2b")

    img = state.preview_image
    h, w = img.shape[:2]

    if img.ndim == 2:
        mode = "Grayscale"
    elif img.shape[2] == 4:
        mode = "RGBA"
    else:
        mode = "RGB"

    filename = state.image_path.split("/")[-1] if state.image_path else "N/A"

    info_frame = tk.Frame(info_win, bg="#3a3a3a", padx=10, pady=10)
    info_frame.pack(fill="x", padx=10, pady=10)

    info_text = f"""Filename: {filename}
Dimensions: {w} x {h}
Channels: {mode}
Type: {img.dtype}
"""

    tk.Label(
        info_frame,
        text=info_text,
        justify="left",
        fg="white",
        bg="#3a3a3a",
        font=("Arial", 11)
    ).pack(anchor="w")

    fig = plt.Figure(figsize=(7, 4), dpi=100)
    fig.patch.set_facecolor("#2b2b2b")

    if img.ndim == 2:
        ax = fig.add_subplot(111)
        ax.hist(img.ravel(), bins=256, color='white')
        ax.set_title("Grayscale Histogram", color="white")
        ax.set_facecolor("#1e1e1e")
        ax.tick_params(colors='white')
    else:
        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(312)
        ax3 = fig.add_subplot(313)

        ax1.hist(img[:, :, 0].ravel(), bins=256, color='red')
        ax1.set_title("Red Channel", color="white")
        ax1.set_facecolor("#1e1e1e")

        ax2.hist(img[:, :, 1].ravel(), bins=256, color='green')
        ax2.set_title("Green Channel")
        ax2.set_facecolor("#1e1e1e")

        ax3.hist(img[:, :, 2].ravel(), bins=256, color='blue')
        ax3.set_title("Blue Channel")
        ax3.set_facecolor("#1e1e1e")

        for ax in (ax1, ax2, ax3):
            ax.tick_params(colors='white')

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=info_win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def reset_all():
    if state.first_image is None:
        return
    state.current_image = state.first_image.copy()
    reset_preview()
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import imagelib as imglib
import matplotlib.pyplot as plt

first_image = None
current_image = None
preview_image = None
second_image = None


DEFAULT_BRIGHTNESS = 0
DEFAULT_CHANNEL_R = 0
DEFAULT_CHANNEL_G = 0
DEFAULT_CHANNEL_B = 0
DEFAULT_TRANSLATION_X = 0
DEFAULT_TRANSLATION_Y = 0
DEFAULT_ROTATION = 0
DEFAULT_BINARIZE_THRESHOLD = 0
DEFAULT_RESOLUTION_SCALE = 1.00
DEFAULT_ALPHA = 0.5
DEFALUT_LOWER_H = 0
DEFALUT_LOWER_S = 0
DEFALUT_LOWER_V = 0
DEFALUT_UPPER_H = 179
DEFALUT_UPPER_S = 255
DEFALUT_UPPER_V = 255
DEFAULT_CANNY_TH1 = 100
DEFALUT_CANNY_TH2 = 200
DEFAULT_SOBEL_TH = 100
DEFAULT_ZOOM = 0.0
DEFAULT_CUT_WIDTH = 100
DEFAULT_CUT_HEIGHT = 100
DEFAULT_ALPHA = 0

DEFAULT_ENABLED_RGB = False
DEFAULT_ENABLED_R = True
DEFAULT_ENABLED_G = True
DEFAULT_ENABLED_B = True
DEFAULT_ENABLE_CROP = False
DEFAULT_ENABLE_BINARIZE = False
DEFAULT_ENABLE_FUSION = False
DEFAULT_ENABLE_HSV = False
DEFAULT_ENABLE_CANNY = False
DEFAULT_ENABLE_SOBEL = False
DEFAULT_ENABLED_NEGATIVE = False
DEFAULT_ENABLED_MONOCHROME = False

def open_image():
    global first_image, current_image, preview_image, image_path

    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if not file_path:
        return

    image_path = file_path

    img_pil = Image.open(file_path)

    # Normalizar modo de imagen
    if img_pil.mode in ("RGBA", "LA") or ("transparency" in img_pil.info):
        img_pil = img_pil.convert("RGBA")
    else:
        img_pil = img_pil.convert("RGB")

    img = np.array(img_pil)

    # Copias base
    first_image = current_image = preview_image = img.copy()

    update_preview()

    h, w = img.shape[:2]

    # Configuración de sliders dependientes de la imagen
    x_translation_slider.config(from_=-w, to=w)
    y_translation_slider.config(from_=-h, to=h)
    width_slider.config(from_=1, to=w)
    height_slider.config(from_=1, to=h)

    width_slider.set(w)
    height_slider.set(h)
    

    # Reset de estados
    rgb_enabled.set(DEFAULT_ENABLED_RGB)
    canny_enabled.set(DEFAULT_ENABLE_CANNY)
    sobel_enabled.set(DEFAULT_ENABLE_SOBEL)
    negative_enabled.set(DEFAULT_ENABLED_NEGATIVE)
    monochrome_enabled.set(DEFAULT_ENABLED_MONOCHROME)
    binarize_enabled.set(DEFAULT_ENABLE_BINARIZE)
    fusion_enabled.set(DEFAULT_ENABLE_FUSION)

    canny_th1_slider.set(DEFAULT_CANNY_TH1)
    canny_th2_slider.set(DEFALUT_CANNY_TH2)
    sobel_th_slider.set(DEFAULT_SOBEL_TH)
    rotation_slider.set(DEFAULT_ROTATION)
    brightness_slider.set(DEFAULT_BRIGHTNESS)
    red_slider.set(DEFAULT_CHANNEL_R)
    green_slider.set(DEFAULT_CHANNEL_G)
    blue_slider.set(DEFAULT_CHANNEL_B)
    x_translation_slider.set(DEFAULT_TRANSLATION_X)
    y_translation_slider.set(DEFAULT_TRANSLATION_Y)
    zoom_slider.set(DEFAULT_ZOOM)
    resolution_slider.set(DEFAULT_RESOLUTION_SCALE)
    alpha_slider.set(DEFAULT_ALPHA)

    var_r.set(DEFAULT_ENABLED_R)
    var_g.set(DEFAULT_ENABLED_G)
    var_b.set(DEFAULT_ENABLED_B)

    h_min.set(0); s_min.set(0); v_min.set(0)
    h_max.set(179); s_max.set(255); v_max.set(255)

def save_image():
    global preview_image 
    
    if preview_image is None:
        messagebox.showwarning("Advertencia", "No hay ninguna imagen cargada para guardar.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png", # Por defecto lo guardará como PNG
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg;*.jpeg"),
            ("Bitmap", "*.bmp"),
            ("All Files", "*.*")
        ],
        title="Guardar imagen como..."
    )
    if not file_path:
        return

    try:
        if preview_image.ndim == 2:
            img_to_save = Image.fromarray(preview_image)
        else:
            if preview_image.shape[2] == 4:
                img_to_save = Image.fromarray(preview_image, "RGBA")
            else:
                img_to_save = Image.fromarray(preview_image[:, :, :3], "RGB")

        img_to_save.save(file_path)
        messagebox.showinfo("Éxito", f"Imagen guardada exitosamente en:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar la imagen:\n{str(e)}")

def display_image(img):
    if img is None:
        return

    # Convertir numpy → PIL
    if img.ndim == 2:
        img_pil = Image.fromarray(img)
    else:
        if img.shape[2] == 4:
            img_pil = Image.fromarray(img, "RGBA")
        else:
            img_pil = Image.fromarray(img[:, :, :3], "RGB")

    # Tamaño del contenedor izquierdo
    cont_w = left_container.winfo_width()
    cont_h = left_container.winfo_height()

    # Valores seguros iniciales
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

    image_label.config(image=img_tk)
    image_label.image = img_tk

def update_preview(event=None):
    global preview_image

    if current_image is None: return

    img = current_image.copy()

    if rgb_enabled.get():
        r, g, b = imglib.extract_rgb_channels(img)
        channels = []
        if var_r.get(): channels.append(r)
        if var_g.get(): channels.append(g)
        if var_b.get(): channels.append(b)

        if channels:
            img = np.zeros_like(img)
            for ch in channels:
                img = img + ch
        else:
            img[:] = 0

    r_val = red_slider.get()
    g_val = green_slider.get()
    b_val = blue_slider.get()

    if r_val != 0: img = imglib.adjust_channel(img, 'R', r_val)
    if g_val != 0: img = imglib.adjust_channel(img, 'G', g_val)
    if b_val != 0: img = imglib.adjust_channel(img, 'B', b_val)

    if monochrome_enabled.get():
        img = imglib.monochrome(img)

    img = imglib.adjust_brightness(img, float(brightness_slider.get()))

    if negative_enabled.get():
        img = imglib.invert_colors(img)

    if binarize_enabled.get():
        img = imglib.binarize(img, binarize_slider.get())

    img = imglib.translate_image(img, int(x_translation_slider.get()), int(y_translation_slider.get()))

    if cut_enabled.get():
        w = min(int(width_slider.get()), img.shape[1])
        h = min(int(height_slider.get()), img.shape[0])
        img = imglib.cut(img, 0, w, 0, h)

    img = imglib.zoom(img, 2**float(zoom_slider.get()))
    img = imglib.reduce_resolution(img, float(resolution_slider.get()))

    if hsv_enabled.get():
        lower = (h_min.get(), s_min.get(), v_min.get())
        upper = (h_max.get(), s_max.get(), v_max.get())
        _, img = imglib.segment_hsv(img, lower, upper)

    if canny_enabled.get():
        img = imglib.canny_edge_detection(img, canny_th1_slider.get(), canny_th2_slider.get())

    if sobel_enabled.get():
        img = imglib.sobel_edge_detection(img, sobel_th_slider.get())

    if rotation_slider.get() != 0:
        img = imglib.rotate_fast(img, rotation_slider.get())
        
    if fusion_enabled.get() and second_image is not None:
        img = imglib.weighted_image_fusion(img, second_image, float(alpha_slider.get()))

    preview_image = img
    display_image(img)

def apply_changes():
    global current_image
    if preview_image is None: return

    current_image = preview_image.copy()
    reset_preview()

    h, w = current_image.shape[:2]
    width_slider.config(from_=1, to=w)
    height_slider.config(from_=1, to=h)
    x_translation_slider.config(from_=-w, to=w)
    y_translation_slider.config(from_=-h, to=h)

def reset_preview():
    brightness_slider.set(0)
    rgb_enabled.set(False)
    var_r.set(True); var_g.set(True); var_b.set(True)
    negative_enabled.set(False)
    monochrome_enabled.set(False)
    binarize_enabled.set(False)
    red_slider.set(0); green_slider.set(0); blue_slider.set(0)
    x_translation_slider.set(0); y_translation_slider.set(0)
    width_slider.set(width_slider.cget("to"))
    height_slider.set(height_slider.cget("to"))
    zoom_slider.set(0.0)
    resolution_slider.set(1.0)
    canny_enabled.set(False)
    sobel_enabled.set(False)
    rotation_slider.set(0)
    h_min.set(0); s_min.set(0); v_min.set(0)
    h_max.set(179); s_max.set(255); v_max.set(255)
    fusion_enabled.set(False)
    alpha_slider.set(0.5)
    canny_th1_slider.set(100)
    canny_th2_slider.set(200)
    sobel_th_slider.set(100)
    update_preview()
    
def load_second_image():
    global second_image

    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if not file_path:
        return

    img = Image.open(file_path).convert("RGB")
    second_image = np.array(img)

def show_image_info():
    if preview_image is None:
        messagebox.showwarning("Advertencia", "No hay imagen cargada.")
        return

    info_win = tk.Toplevel(window)
    info_win.title("Image Info")
    info_win.geometry("800x600")
    info_win.configure(bg="#2b2b2b")

    img = preview_image
    h, w = img.shape[:2]

    if img.ndim == 2:
        mode = "Grayscale"
    elif img.shape[2] == 4:
        mode = "RGBA"
    else:
        mode = "RGB"

    filename = image_path.split("/")[-1] if image_path else "N/A"

    # ---------------- INFO PANEL ----------------
    info_frame = tk.Frame(info_win, bg="#3a3a3a", padx=10, pady=10)
    info_frame.pack(fill="x", padx=10, pady=10)

    info_text = f"""
Filename: {filename}
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

    # ---------------- HISTOGRAM PANEL ----------------
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

        # Rojo
        ax1.hist(img[:, :, 0].ravel(), bins=256, color='red')
        ax1.set_title("Red Channel")
        ax1.set_facecolor("#1e1e1e")

        # Verde
        ax2.hist(img[:, :, 1].ravel(), bins=256, color='green')
        ax2.set_title("Green Channel")
        ax2.set_facecolor("#1e1e1e")

        # Azul
        ax3.hist(img[:, :, 2].ravel(), bins=256, color='blue')
        ax3.set_title("Blue Channel")
        ax3.set_facecolor("#1e1e1e")

        for ax in [ax1, ax2, ax3]:
            ax.tick_params(colors='white')

    fig.tight_layout()

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    canvas = FigureCanvasTkAgg(fig, master=info_win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def reset_all():
    global current_image
    if first_image is None: return
    current_image = first_image.copy()
    reset_preview()

window = tk.Tk()
window.title("Picto - Image Editor")
window.geometry("1300x700")

# ---------------- BARRA DE ACCIONES ----------------
action_bar = tk.Frame(window, relief="raised", bd=2, bg="#f0f0f0")
action_bar.pack(side="top", fill="x", padx=5, pady=5)

left_actions = tk.Frame(action_bar, bg="#f0f0f0")
left_actions.pack(side="left")

tk.Button(left_actions, text="Open Image", command=open_image, width=12).pack(side="left", padx=10, pady=5)
tk.Button(left_actions, text="Apply Changes", bg="#ccffcc", font=("Arial", 9, "bold"), command=apply_changes, width=15).pack(side="left", padx=10, pady=5)
tk.Button(left_actions, text="Reset Preview", command=reset_preview, width=15).pack(side="left", padx=10, pady=5)
tk.Button(left_actions, text="Reset All", bg="#ffcccc", command=reset_all, width=12).pack(side="left", padx=10, pady=5)

right_actions = tk.Frame(action_bar, bg="#f0f0f0")
right_actions.pack(side="right")

tk.Button(right_actions, text="Save Image", bg="#cce6ff", command=save_image, width=12).pack(side="right", padx=10, pady=5)

# ---------------- CONTENEDOR PRINCIPAL (CON PANEDWINDOW) ----------------
# Reemplazamos el tk.Frame por tk.PanedWindow
main_layout = tk.PanedWindow(window, orient="horizontal", sashrelief="raised", sashwidth=6, bg="#ccc")
main_layout.pack(fill="both", expand=True)

# Lado Izquierdo (Imagen)
left_container = tk.Frame(main_layout, bg="#333")
image_label = tk.Label(left_container, bg="#333")
image_label.pack(expand=True)

# Lado Derecho (Controles)
right_canvas_frame = tk.Frame(main_layout, width=450) # Ancho inicial más razonable

# Añadimos los frames al PanedWindow
main_layout.add(left_container, stretch="always", minsize=400) # La imagen intenta usar el espacio extra
main_layout.add(right_canvas_frame, stretch="never", minsize=300) # Los controles mantienen su tamaño
# ---------------- SCROLLS (VERTICAL Y HORIZONTAL) ----------------
v_scrollbar = ttk.Scrollbar(right_canvas_frame, orient="vertical")
h_scrollbar = ttk.Scrollbar(right_canvas_frame, orient="horizontal")

canvas = tk.Canvas(right_canvas_frame, width=680, yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

v_scrollbar.config(command=canvas.yview)
h_scrollbar.config(command=canvas.xview)

v_scrollbar.pack(side="right", fill="y")
h_scrollbar.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# ---------------- COLUMNAS Y CONTROLES ----------------
cols = [tk.Frame(scrollable_frame) for _ in range(4)]
for c in cols:
    c.pack(side="left", fill="y", padx=5, anchor="n")

col1, col2, col3, col4 = cols

frame_brightness = tk.LabelFrame(col1, text="Brightness")
frame_brightness.pack(fill="x", pady=5)
brightness_slider = tk.Scale(frame_brightness, from_=-1, to=1, resolution=0.01, orient="horizontal", command=update_preview)
brightness_slider.pack(fill="x")
brightness_reset_button = tk.Button(frame_brightness, text="Default", command=lambda: brightness_slider.set(DEFAULT_BRIGHTNESS))
brightness_reset_button.pack(fill="x", pady=2)


frame_rgb = tk.LabelFrame(col1, text="RGB Channels")
frame_rgb.pack(fill="x", pady=5)
rgb_enabled = tk.BooleanVar()
var_r = tk.BooleanVar(value=True)
var_g = tk.BooleanVar(value=True)
var_b = tk.BooleanVar(value=True)
tk.Checkbutton(frame_rgb, text="Enable RGB", variable=rgb_enabled, command=update_preview).pack(anchor="w")
tk.Checkbutton(frame_rgb, text="Red", variable=var_r, command=update_preview).pack(anchor="w")
tk.Checkbutton(frame_rgb, text="Green", variable=var_g, command=update_preview).pack(anchor="w")
tk.Checkbutton(frame_rgb, text="Blue", variable=var_b, command=update_preview).pack(anchor="w")

frame_chanadjust = tk.LabelFrame(col1, text="Channel Adjusters")
frame_chanadjust.pack(fill="x", pady=5)
red_slider = tk.Scale(frame_chanadjust, from_=-100, to=100, orient="horizontal", label="Red", command=update_preview)
red_slider.pack(fill="x")
red_reset_button = tk.Button(frame_chanadjust, text="Default", command=lambda: red_slider.set(DEFAULT_CHANNEL_R))
red_reset_button.pack(fill="x", pady=2)


green_slider = tk.Scale(frame_chanadjust, from_=-100, to=100, orient="horizontal", label="Green", command=update_preview)
green_slider.pack(fill="x")
green_reset_button = tk.Button(frame_chanadjust, text="Default", command=lambda: green_slider.set(DEFAULT_CHANNEL_G))
green_reset_button.pack(fill="x", pady=2)

blue_slider = tk.Scale(frame_chanadjust, from_=-100, to=100, orient="horizontal", label="Blue", command=update_preview)
blue_slider.pack(fill="x")
blue_reset_button = tk.Button(frame_chanadjust, text="Default", command=lambda: blue_slider.set(DEFAULT_CHANNEL_B))
blue_reset_button.pack(fill="x", pady=2)



frame_translation = tk.LabelFrame(col2, text="Translation")
frame_translation.pack(fill="x", pady=5)
x_translation_slider = tk.Scale(frame_translation, from_=-100, to=100, orient="horizontal", label="X", command=update_preview)
x_translation_slider.pack(fill="x")
x_translation_reset_button = tk.Button(frame_translation, text="Default", command=lambda: x_translation_slider.set(DEFAULT_TRANSLATION_X))
x_translation_reset_button.pack(fill="x", pady=2)


y_translation_slider = tk.Scale(frame_translation, from_=-100, to=100, orient="horizontal", label="Y", command=update_preview)
y_translation_slider.pack(fill="x")
y_translation_reset_button = tk.Button(frame_translation, text="Default", command=lambda: y_translation_slider.set(DEFAULT_TRANSLATION_Y))
y_translation_reset_button.pack(fill="x", pady=2)


rotation_frame = tk.LabelFrame(col2, text="Rotation")
rotation_frame.pack(fill="x", pady=5)
rotation_slider = tk.Scale(rotation_frame, from_=-180, to=180, orient="horizontal", command=update_preview)
rotation_slider.pack(fill="x")
rotation_reset_button = tk.Button(rotation_frame, text="Default", command=lambda: rotation_slider.set(DEFAULT_ROTATION))
rotation_reset_button.pack(fill="x", pady=2)


frame_cut = tk.LabelFrame(col2, text="Crop")
frame_cut.pack(fill="x", pady=5)
cut_enabled = tk.BooleanVar()
tk.Checkbutton(frame_cut, text="Enable", variable=cut_enabled, command=update_preview).pack(anchor="w")
width_slider = tk.Scale(frame_cut, from_=1, to=500, orient="horizontal", command=update_preview)
width_slider.pack(fill="x")
width_reset_button = tk.Button(frame_cut, text="Default", command=lambda: width_slider.set(DEFAULT_CUT_WIDTH))
width_reset_button.pack(fill="x", pady=2)


height_slider = tk.Scale(frame_cut, from_=1, to=500, orient="horizontal", command=update_preview)
height_slider.pack(fill="x")

frame_zoom = tk.LabelFrame(col2, text="Zoom")
frame_zoom.pack(fill="x", pady=5)
zoom_slider = tk.Scale(frame_zoom, from_=-5, to=5, resolution=0.05, orient="horizontal", command=update_preview)
zoom_slider.pack(fill="x")

frame_filters = tk.LabelFrame(col3, text="Color Effects")
frame_filters.pack(fill="x", pady=5)
negative_enabled = tk.BooleanVar()
monochrome_enabled = tk.BooleanVar()
tk.Checkbutton(frame_filters, text="Negative", variable=negative_enabled, command=update_preview).pack(anchor="w")
tk.Checkbutton(frame_filters, text="Monochrome", variable=monochrome_enabled, command=update_preview).pack(anchor="w")

frame_binarize = tk.LabelFrame(col3, text="Binarize")
frame_binarize.pack(fill="x", pady=5)
binarize_enabled = tk.BooleanVar()
tk.Checkbutton(frame_binarize, text="Enable", variable=binarize_enabled, command=update_preview).pack(anchor="w")
binarize_slider = tk.Scale(frame_binarize, from_=0, to=255, orient="horizontal", command=update_preview)
binarize_slider.pack(fill="x")

frame_resolution = tk.LabelFrame(col3, text="Resolution")
frame_resolution.pack(fill="x", pady=5)
resolution_slider = tk.Scale(frame_resolution, from_=0, to=1.0, resolution=0.001, orient="horizontal", command=update_preview)
resolution_slider.pack(fill="x")
resolution_slider.set(1.0)

frame_hsv = tk.LabelFrame(col4, text="HSV Segmentation")
frame_hsv.pack(fill="x", pady=5)

hsv_enabled = tk.BooleanVar()
tk.Checkbutton(frame_hsv, text="Enable HSV", variable=hsv_enabled, command=update_preview).pack(anchor="w")

tk.Label(frame_hsv, text="Lower").pack()
h_min = tk.Scale(frame_hsv, from_=0, to=179, orient="horizontal", command=update_preview)
h_min.pack(fill="x")
s_min = tk.Scale(frame_hsv, from_=0, to=255, orient="horizontal", command=update_preview)
s_min.pack(fill="x")
v_min = tk.Scale(frame_hsv, from_=0, to=255, orient="horizontal", command=update_preview)
v_min.pack(fill="x")

tk.Label(frame_hsv, text="Upper").pack()
h_max = tk.Scale(frame_hsv, from_=0, to=179, orient="horizontal", command=update_preview)
h_max.set(179)
h_max.pack(fill="x")
s_max = tk.Scale(frame_hsv, from_=0, to=255, orient="horizontal", command=update_preview)
s_max.set(255)
s_max.pack(fill="x")
v_max = tk.Scale(frame_hsv, from_=0, to=255, orient="horizontal", command=update_preview)
v_max.set(255)
v_max.pack(fill="x")

canny_frame = tk.LabelFrame(col4, text="Canny")
canny_frame.pack(fill="x", pady=5)
canny_enabled = tk.BooleanVar()
tk.Checkbutton(canny_frame, text="Enable", variable=canny_enabled, command=update_preview).pack(anchor="w")
canny_th1_slider = tk.Scale(canny_frame, from_=0, to=255, orient="horizontal", command=update_preview)
canny_th1_slider.pack(fill="x")
canny_th2_slider = tk.Scale(canny_frame, from_=0, to=255, orient="horizontal", command=update_preview)
canny_th2_slider.pack(fill="x")
canny_th1_slider.set(100)
canny_th2_slider.set(200)

sobel_frame = tk.LabelFrame(col4, text="Sobel")
sobel_frame.pack(fill="x", pady=5)
sobel_enabled = tk.BooleanVar()
tk.Checkbutton(sobel_frame, text="Enable", variable=sobel_enabled, command=update_preview).pack(anchor="w")
sobel_th_slider = tk.Scale(sobel_frame, from_=0, to=255, orient="horizontal", command=update_preview)
sobel_th_slider.pack(fill="x")
sobel_th_slider.set(100)

frame_fusion = tk.LabelFrame(col3, text="Image Fusion")
frame_fusion.pack(fill="x", pady=5)
fusion_enabled = tk.BooleanVar()
tk.Checkbutton(frame_fusion, text="Enable Fusion", variable=fusion_enabled, command=update_preview).pack(anchor="w")
tk.Button(frame_fusion, text="Load Image 2", command=load_second_image).pack(fill="x")
alpha_slider = tk.Scale(frame_fusion, from_=0.0, to=1.0, resolution=0.01, orient="horizontal", label="Alpha", command=update_preview)
alpha_slider.set(0.5)
alpha_slider.pack(fill="x")

frame_data = tk.LabelFrame(col3, text="Data Analysis")
frame_data.pack(fill="x", pady=5)
histogram_button = tk.Button(frame_data, text="Show Image Info", command=show_image_info)
histogram_button.pack(fill="x")


# ---------------- EVENTOS DEL RATÓN ----------------
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def _on_shift_mousewheel(event):
    canvas.xview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

# --- NUEVO EVENTO DE REDIMENSIONAMIENTO ---
def _on_resize_container(event):
    # Solo actualizamos si ya hay una imagen cargada para evitar errores
    if preview_image is not None:
        display_image(preview_image)

canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

# Conectamos el evento de redimensionamiento al contenedor izquierdo
left_container.bind("<Configure>", _on_resize_container)

window.mainloop()
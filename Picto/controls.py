# Este módulo actúa como registro compartido de widgets.
# ui.py escribe los atributos aquí al construir la interfaz.
# actions.py los lee para operar sobre ellos.
# No instanciar nada aquí: todo llega desde ui.py.

# --- Sliders ---
brightness_slider = None
red_slider = None
green_slider = None
blue_slider = None
x_translation_slider = None
y_translation_slider = None
rotation_slider = None
width_slider = None
height_slider = None
zoom_slider = None
resolution_slider = None
alpha_slider = None
binarize_slider = None
canny_th1_slider = None
canny_th2_slider = None
sobel_th_slider = None
h_min = None
s_min = None
v_min = None
h_max = None
s_max = None
v_max = None

# --- BooleanVars (checkboxes) ---
rgb_enabled = None
var_r = None
var_g = None
var_b = None
negative_enabled = None
monochrome_enabled = None
binarize_enabled = None
cut_enabled = None
fusion_enabled = None
hsv_enabled = None
canny_enabled = None
sobel_enabled = None

# --- Widgets de visualización ---
image_label = None
left_container = None
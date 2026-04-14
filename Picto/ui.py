import tkinter as tk
from tkinter import ttk

import controls as ctrl
import actions
from constants import (
    DEFAULT_BRIGHTNESS, DEFAULT_CHANNEL_R, DEFAULT_CHANNEL_G, DEFAULT_CHANNEL_B,
    DEFAULT_TRANSLATION_X, DEFAULT_TRANSLATION_Y, DEFAULT_ROTATION,
    DEFAULT_BINARIZE_THRESHOLD, DEFAULT_RESOLUTION_SCALE, DEFAULT_ALPHA,
    DEFALUT_LOWER_H, DEFALUT_LOWER_S, DEFALUT_LOWER_V,
    DEFALUT_UPPER_H, DEFALUT_UPPER_S, DEFALUT_UPPER_V,
    DEFAULT_CANNY_TH1, DEFAULT_CANNY_TH2, DEFAULT_SOBEL_TH, DEFAULT_ZOOM,
    DEFAULT_ENABLED_R, DEFAULT_ENABLED_G, DEFAULT_ENABLED_B,
)


def build(window):
    # ---------------- BARRA DE ACCIONES ----------------
    action_bar = tk.Frame(window, relief="raised", bd=2, bg="#f0f0f0")
    action_bar.pack(side="top", fill="x", padx=5, pady=5)

    left_actions = tk.Frame(action_bar, bg="#f0f0f0")
    left_actions.pack(side="left")

    tk.Button(left_actions, text="Open Image", command=actions.open_image, width=12).pack(side="left", padx=10, pady=5)
    tk.Button(left_actions, text="Apply Changes", bg="#ccffcc", font=("Arial", 9, "bold"), command=actions.apply_changes, width=15).pack(side="left", padx=10, pady=5)
    tk.Button(left_actions, text="Reset Preview", command=actions.reset_preview, width=15).pack(side="left", padx=10, pady=5)
    tk.Button(left_actions, text="Reset All", bg="#ffcccc", command=actions.reset_all, width=12).pack(side="left", padx=10, pady=5)

    right_actions = tk.Frame(action_bar, bg="#f0f0f0")
    right_actions.pack(side="right")

    tk.Button(right_actions, text="Save Image", bg="#cce6ff", command=actions.save_image, width=12).pack(side="right", padx=10, pady=5)

    # ---------------- CONTENEDOR PRINCIPAL ----------------
    main_layout = tk.PanedWindow(window, orient="horizontal", sashrelief="raised", sashwidth=6, bg="#ccc")
    main_layout.pack(fill="both", expand=True)

    left_container = tk.Frame(main_layout, bg="#333")
    image_label = tk.Label(left_container, bg="#333")
    image_label.pack(expand=True)

    right_canvas_frame = tk.Frame(main_layout, width=450)

    main_layout.add(left_container, stretch="always", minsize=400)
    main_layout.add(right_canvas_frame, stretch="never", minsize=300)

    # Registrar en controls
    ctrl.left_container = left_container
    ctrl.image_label = image_label

    # ---------------- SCROLLS ----------------
    v_scrollbar = ttk.Scrollbar(right_canvas_frame, orient="vertical")
    h_scrollbar = ttk.Scrollbar(right_canvas_frame, orient="horizontal")

    canvas = tk.Canvas(
        right_canvas_frame,
        width=680,
        yscrollcommand=v_scrollbar.set,
        xscrollcommand=h_scrollbar.set
    )

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

    # ---------------- COLUMNAS ----------------
    cols = [tk.Frame(scrollable_frame) for _ in range(4)]
    for c in cols:
        c.pack(side="left", fill="y", padx=5, anchor="n")

    col1, col2, col3, col4 = cols

    # ---- COL 1 ----

    frame_brightness = tk.LabelFrame(col1, text="Brightness")
    frame_brightness.pack(fill="x", pady=5)
    ctrl.brightness_slider = tk.Scale(frame_brightness, from_=-1, to=1, resolution=0.01, orient="horizontal", command=actions.update_preview)
    ctrl.brightness_slider.pack(fill="x")
    tk.Button(frame_brightness, text="Default", command=lambda: ctrl.brightness_slider.set(DEFAULT_BRIGHTNESS)).pack(fill="x", pady=2)

    frame_rgb = tk.LabelFrame(col1, text="RGB Channels")
    frame_rgb.pack(fill="x", pady=5)
    ctrl.rgb_enabled = tk.BooleanVar()
    ctrl.var_r = tk.BooleanVar(value=True)
    ctrl.var_g = tk.BooleanVar(value=True)
    ctrl.var_b = tk.BooleanVar(value=True)
    tk.Checkbutton(frame_rgb, text="Enable RGB", variable=ctrl.rgb_enabled, command=actions.update_preview).pack(anchor="w")
    tk.Checkbutton(frame_rgb, text="Red", variable=ctrl.var_r, command=actions.update_preview).pack(anchor="w")
    tk.Checkbutton(frame_rgb, text="Green", variable=ctrl.var_g, command=actions.update_preview).pack(anchor="w")
    tk.Checkbutton(frame_rgb, text="Blue", variable=ctrl.var_b, command=actions.update_preview).pack(anchor="w")

    frame_chanadjust = tk.LabelFrame(col1, text="Channel Adjusters")
    frame_chanadjust.pack(fill="x", pady=5)
    ctrl.red_slider = tk.Scale(frame_chanadjust, from_=-100, to=100, orient="horizontal", label="Red", command=actions.update_preview)
    ctrl.red_slider.pack(fill="x")
    tk.Button(frame_chanadjust, text="Default", command=lambda: ctrl.red_slider.set(DEFAULT_CHANNEL_R)).pack(fill="x", pady=2)

    ctrl.green_slider = tk.Scale(frame_chanadjust, from_=-100, to=100, orient="horizontal", label="Green", command=actions.update_preview)
    ctrl.green_slider.pack(fill="x")
    tk.Button(frame_chanadjust, text="Default", command=lambda: ctrl.green_slider.set(DEFAULT_CHANNEL_G)).pack(fill="x", pady=2)

    ctrl.blue_slider = tk.Scale(frame_chanadjust, from_=-100, to=100, orient="horizontal", label="Blue", command=actions.update_preview)
    ctrl.blue_slider.pack(fill="x")
    tk.Button(frame_chanadjust, text="Default", command=lambda: ctrl.blue_slider.set(DEFAULT_CHANNEL_B)).pack(fill="x", pady=2)

    # ---- COL 2 ----

    frame_translation = tk.LabelFrame(col2, text="Translation")
    frame_translation.pack(fill="x", pady=5)
    ctrl.x_translation_slider = tk.Scale(frame_translation, from_=-100, to=100, orient="horizontal", label="X", command=actions.update_preview)
    ctrl.x_translation_slider.pack(fill="x")
    tk.Button(frame_translation, text="Default", command=lambda: ctrl.x_translation_slider.set(DEFAULT_TRANSLATION_X)).pack(fill="x", pady=2)

    ctrl.y_translation_slider = tk.Scale(frame_translation, from_=-100, to=100, orient="horizontal", label="Y", command=actions.update_preview)
    ctrl.y_translation_slider.pack(fill="x")
    tk.Button(frame_translation, text="Default", command=lambda: ctrl.y_translation_slider.set(DEFAULT_TRANSLATION_Y)).pack(fill="x", pady=2)

    rotation_frame = tk.LabelFrame(col2, text="Rotation")
    rotation_frame.pack(fill="x", pady=5)
    ctrl.rotation_slider = tk.Scale(rotation_frame, from_=-180, to=180, orient="horizontal", command=actions.update_preview)
    ctrl.rotation_slider.pack(fill="x")
    tk.Button(rotation_frame, text="Default", command=lambda: ctrl.rotation_slider.set(DEFAULT_ROTATION)).pack(fill="x", pady=2)

    frame_cut = tk.LabelFrame(col2, text="Crop")
    frame_cut.pack(fill="x", pady=5)
    ctrl.cut_enabled = tk.BooleanVar()
    tk.Checkbutton(frame_cut, text="Enable", variable=ctrl.cut_enabled, command=actions.update_preview).pack(anchor="w")
    ctrl.width_slider = tk.Scale(frame_cut, from_=1, to=500, orient="horizontal", command=actions.update_preview)
    ctrl.width_slider.pack(fill="x")
    tk.Button(frame_cut, text="Default", command=lambda: ctrl.width_slider.set(int(ctrl.width_slider.cget("to")))).pack(fill="x", pady=2)

    ctrl.height_slider = tk.Scale(frame_cut, from_=1, to=500, orient="horizontal", command=actions.update_preview)
    ctrl.height_slider.pack(fill="x")
    tk.Button(frame_cut, text="Default", command=lambda: ctrl.height_slider.set(int(ctrl.height_slider.cget("to")))).pack(fill="x", pady=2)

    frame_zoom = tk.LabelFrame(col2, text="Zoom")
    frame_zoom.pack(fill="x", pady=5)
    ctrl.zoom_slider = tk.Scale(frame_zoom, from_=-5, to=5, resolution=0.05, orient="horizontal", command=actions.update_preview)
    ctrl.zoom_slider.pack(fill="x")
    tk.Button(frame_zoom, text="Default", command=lambda: ctrl.zoom_slider.set(DEFAULT_ZOOM)).pack(fill="x", pady=2)

    # ---- COL 3 ----

    frame_filters = tk.LabelFrame(col3, text="Color Effects")
    frame_filters.pack(fill="x", pady=5)
    ctrl.negative_enabled = tk.BooleanVar()
    ctrl.monochrome_enabled = tk.BooleanVar()
    tk.Checkbutton(frame_filters, text="Negative", variable=ctrl.negative_enabled, command=actions.update_preview).pack(anchor="w")
    tk.Checkbutton(frame_filters, text="Monochrome", variable=ctrl.monochrome_enabled, command=actions.update_preview).pack(anchor="w")

    frame_binarize = tk.LabelFrame(col3, text="Binarize")
    frame_binarize.pack(fill="x", pady=5)
    ctrl.binarize_enabled = tk.BooleanVar()
    tk.Checkbutton(frame_binarize, text="Enable", variable=ctrl.binarize_enabled, command=actions.update_preview).pack(anchor="w")
    ctrl.binarize_slider = tk.Scale(frame_binarize, from_=0, to=255, orient="horizontal", command=actions.update_preview)
    ctrl.binarize_slider.pack(fill="x")
    tk.Button(frame_binarize, text="Default", command=lambda: ctrl.binarize_slider.set(DEFAULT_BINARIZE_THRESHOLD)).pack(fill="x", pady=2)

    frame_resolution = tk.LabelFrame(col3, text="Resolution")
    frame_resolution.pack(fill="x", pady=5)
    ctrl.resolution_slider = tk.Scale(frame_resolution, from_=0, to=1.0, resolution=0.001, orient="horizontal", command=actions.update_preview)
    ctrl.resolution_slider.pack(fill="x")
    ctrl.resolution_slider.set(1.0)
    tk.Button(frame_resolution, text="Default", command=lambda: ctrl.resolution_slider.set(DEFAULT_RESOLUTION_SCALE)).pack(fill="x", pady=2)

    frame_fusion = tk.LabelFrame(col3, text="Image Fusion")
    frame_fusion.pack(fill="x", pady=5)
    ctrl.fusion_enabled = tk.BooleanVar()
    tk.Checkbutton(frame_fusion, text="Enable Fusion", variable=ctrl.fusion_enabled, command=actions.update_preview).pack(anchor="w")
    tk.Button(frame_fusion, text="Load Image 2", command=actions.load_second_image).pack(fill="x")
    ctrl.alpha_slider = tk.Scale(frame_fusion, from_=0.0, to=1.0, resolution=0.01, orient="horizontal", label="Alpha", command=actions.update_preview)
    ctrl.alpha_slider.set(0.5)
    ctrl.alpha_slider.pack(fill="x")
    tk.Button(frame_fusion, text="Default", command=lambda: ctrl.alpha_slider.set(DEFAULT_ALPHA)).pack(fill="x", pady=2)

    frame_data = tk.LabelFrame(col3, text="Data Analysis")
    frame_data.pack(fill="x", pady=5)
    tk.Button(frame_data, text="Show Image Info", command=actions.show_image_info).pack(fill="x")

    # ---- COL 4 ----

    frame_hsv = tk.LabelFrame(col4, text="HSV Segmentation")
    frame_hsv.pack(fill="x", pady=5)
    ctrl.hsv_enabled = tk.BooleanVar()
    tk.Checkbutton(frame_hsv, text="Enable HSV", variable=ctrl.hsv_enabled, command=actions.update_preview).pack(anchor="w")

    tk.Label(frame_hsv, text="Lower").pack()
    ctrl.h_min = tk.Scale(frame_hsv, from_=0, to=179, orient="horizontal", command=actions.update_preview)
    ctrl.h_min.pack(fill="x")
    tk.Button(frame_hsv, text="Default", command=lambda: ctrl.h_min.set(DEFALUT_LOWER_H)).pack(fill="x", pady=2)

    ctrl.s_min = tk.Scale(frame_hsv, from_=0, to=255, orient="horizontal", command=actions.update_preview)
    ctrl.s_min.pack(fill="x")
    tk.Button(frame_hsv, text="Default", command=lambda: ctrl.s_min.set(DEFALUT_LOWER_S)).pack(fill="x", pady=2)

    ctrl.v_min = tk.Scale(frame_hsv, from_=0, to=255, orient="horizontal", command=actions.update_preview)
    ctrl.v_min.pack(fill="x")
    tk.Button(frame_hsv, text="Default", command=lambda: ctrl.v_min.set(DEFALUT_LOWER_V)).pack(fill="x", pady=2)

    tk.Label(frame_hsv, text="Upper").pack()
    ctrl.h_max = tk.Scale(frame_hsv, from_=0, to=179, orient="horizontal", command=actions.update_preview)
    ctrl.h_max.set(179)
    ctrl.h_max.pack(fill="x")
    tk.Button(frame_hsv, text="Default", command=lambda: ctrl.h_max.set(DEFALUT_UPPER_H)).pack(fill="x", pady=2)

    ctrl.s_max = tk.Scale(frame_hsv, from_=0, to=255, orient="horizontal", command=actions.update_preview)
    ctrl.s_max.set(255)
    ctrl.s_max.pack(fill="x")
    tk.Button(frame_hsv, text="Default", command=lambda: ctrl.s_max.set(DEFALUT_UPPER_S)).pack(fill="x", pady=2)

    ctrl.v_max = tk.Scale(frame_hsv, from_=0, to=255, orient="horizontal", command=actions.update_preview)
    ctrl.v_max.set(255)
    ctrl.v_max.pack(fill="x")
    tk.Button(frame_hsv, text="Default", command=lambda: ctrl.v_max.set(DEFALUT_UPPER_V)).pack(fill="x", pady=2)

    canny_frame = tk.LabelFrame(col4, text="Canny")
    canny_frame.pack(fill="x", pady=5)
    ctrl.canny_enabled = tk.BooleanVar()
    tk.Checkbutton(canny_frame, text="Enable", variable=ctrl.canny_enabled, command=actions.update_preview).pack(anchor="w")
    ctrl.canny_th1_slider = tk.Scale(canny_frame, from_=0, to=255, orient="horizontal", command=actions.update_preview)
    ctrl.canny_th1_slider.pack(fill="x")
    tk.Button(canny_frame, text="Default", command=lambda: ctrl.canny_th1_slider.set(DEFAULT_CANNY_TH1)).pack(fill="x", pady=2)

    ctrl.canny_th2_slider = tk.Scale(canny_frame, from_=0, to=255, orient="horizontal", command=actions.update_preview)
    ctrl.canny_th2_slider.pack(fill="x")
    tk.Button(canny_frame, text="Default", command=lambda: ctrl.canny_th2_slider.set(DEFAULT_CANNY_TH2)).pack(fill="x", pady=2)
    ctrl.canny_th1_slider.set(100)
    ctrl.canny_th2_slider.set(200)

    sobel_frame = tk.LabelFrame(col4, text="Sobel")
    sobel_frame.pack(fill="x", pady=5)
    ctrl.sobel_enabled = tk.BooleanVar()
    tk.Checkbutton(sobel_frame, text="Enable", variable=ctrl.sobel_enabled, command=actions.update_preview).pack(anchor="w")
    ctrl.sobel_th_slider = tk.Scale(sobel_frame, from_=0, to=255, orient="horizontal", command=actions.update_preview)
    ctrl.sobel_th_slider.pack(fill="x")
    ctrl.sobel_th_slider.set(100)
    tk.Button(sobel_frame, text="Default", command=lambda: ctrl.sobel_th_slider.set(DEFAULT_SOBEL_TH)).pack(fill="x", pady=2)

    # ---------------- EVENTOS ----------------
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mousewheel(event):
        canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_resize_container(event):
        import state
        if state.preview_image is not None:
            actions.display_image(state.preview_image)

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)
    left_container.bind("<Configure>", _on_resize_container)
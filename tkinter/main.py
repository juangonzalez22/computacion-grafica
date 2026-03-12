import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

ventana = tk.Tk()
ventana.title("Mi primera ventana")
ventana.geometry("400x300")

ventana.resizable(False, False)
ventana.configure(bg="lightblue")

etiqueta = tk.Label(ventana, text="¡Hola, Mundo!", font=("Arial", 16), fg="black", bg="lightblue")

etiqueta.place(x=150, y=130)
ventana.mainloop()


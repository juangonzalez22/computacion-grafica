import tkinter as tk
import ui


def main():
    window = tk.Tk()
    window.title("Picto - Image Editor")
    window.geometry("1300x700")
    window.iconbitmap("PictoLogo.ico")

    ui.build(window)

    window.mainloop()


if __name__ == "__main__":
    main()
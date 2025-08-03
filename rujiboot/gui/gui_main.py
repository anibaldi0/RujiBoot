# File: gui/gui_main.py
# GUI interface entry point for RujiBoot (Tkinter-based)

import tkinter as tk
from tkinter import messagebox
from utils.i18n_util import load_translations

current_language = "en"  # podés setearlo dinámicamente

def run_gui():
    t = load_translations(current_language)

    root = tk.Tk()
    root.title("RujiBoot")
    root.geometry("400x200")

    label = tk.Label(
        root,
        text=t.get("welcome_message", "Welcome to RujiBoot"),
        font=("Arial", 12),
        justify="center"
    )
    label.pack(expand=True)

    def on_close():
        if messagebox.askokcancel(
            t.get("exit_title", "Quit"),
            t.get("exit_prompt", "Do you want to exit?")
        ):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

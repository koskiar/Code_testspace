import tkinter as tk
from gui.styles import apply_styles
from gui.layout import MainUI

def launch_app():
    root = tk.Tk()
    apply_styles(root)
    ui = MainUI(root)
    ui.runner.load_definitions()
    ui.history.load_history_list()
    root.mainloop()

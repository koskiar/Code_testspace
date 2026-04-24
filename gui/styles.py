import tkinter as tk
from tkinter import ttk

LIGHT_BG = "#f0f2f5"
LIGHT_PANEL = "#ffffff"
LIGHT_CARD = "#e6e6e6"
LIGHT_TEXT = "#222222"

DARK_BG = "#1e1f23"
DARK_PANEL = "#2a2c31"
DARK_CARD = "#33353b"
DARK_TEXT = "#f5f5f5"

PRIMARY = "#0078d7"
PRIMARY_DARK = "#005a9e"

STATUS_NOTRUN = "#d9d9d9"
STATUS_RUNNING = "#fff3cd"
STATUS_PASSED = "#d4edda"
STATUS_FAILED = "#f8d7da"


def apply_styles(root: tk.Tk, dark_mode: bool = False):
    style = ttk.Style(root)
    style.theme_use("clam")

    if dark_mode:
        bg = DARK_BG
        panel = DARK_PANEL
        card = DARK_CARD
        text = DARK_TEXT
        entry_bg = "#3a3c42"
        entry_fg = DARK_TEXT
    else:
        bg = LIGHT_BG
        panel = LIGHT_PANEL
        card = LIGHT_CARD
        text = LIGHT_TEXT
        entry_bg = "#ffffff"
        entry_fg = LIGHT_TEXT

    root.configure(background=bg)

    # Main frames
    style.configure("Main.TFrame", background=bg)

    # Header
    style.configure("Header.TFrame", background=bg)
    style.configure("HeaderInner.TFrame", background=panel)
    style.configure("Header.TLabel", background=panel, foreground=text, font=("Segoe UI", 11))
    style.configure("Header.TButton", font=("Segoe UI", 10, "bold"), padding=(10, 5))

    # Central block (card)
    style.configure("CentralBlock.TFrame", background=card, relief="ridge", borderwidth=2)

    # LabelFrames
    style.configure("Sequence.TLabelframe", background=bg)
    style.configure("Sequence.TLabelframe.Label", foreground=text, font=("Segoe UI", 10, "bold"))

    style.configure("History.TLabelframe", background=bg)
    style.configure("History.TLabelframe.Label", foreground=text, font=("Segoe UI", 10, "bold"))

    # Status bar
    style.configure("Status.TLabel", background=card, foreground=text, font=("Segoe UI", 9))

    # Treeview
    style.configure(
        "Custom.Treeview",
        font=("Segoe UI", 10),
        rowheight=28,
        background=panel,
        fieldbackground=panel,
        foreground=text,
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background=card,
        foreground=text
    )
    style.map(
        "Custom.Treeview",
        background=[("selected", PRIMARY)],
        foreground=[("selected", "#ffffff")]
    )

    # Progressbars
    style.configure(
        "Horizontal.TProgressbar",
        troughcolor="#bfbfbf" if not dark_mode else "#44464d",
        background=PRIMARY,
        lightcolor=PRIMARY,
        darkcolor=PRIMARY_DARK
    )

    # Buttons
    style.configure("TButton", background=panel, foreground=text)

    # Entry defaults
    root.option_clear()
    root.option_add("*TEntry*background", entry_bg)
    root.option_add("*TEntry*foreground", entry_fg)
    root.option_add("*TEntry*insertBackground", entry_fg)

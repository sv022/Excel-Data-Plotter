from tkinter import ttk


colors = {
    "white": "#ffffff",
    "graphite": "#3b3b3b",
    "green": "#009063",
    "light-purple": "#e3e0f3",
    "red": "#ff2a40",
    "muted": "#808080"
}


stylesheet = {
    "btn-primary": {
        "font": ("Arial", 9),
        "borderwidth": 1,
        "foreground": colors['graphite'],
        "bordercolor": colors['green'],
    },
    "btn-clear": {
        "font": ("Arial", 8),
        "foreground": colors['red'],
        "borderwidth": 1,
    },
    "btn-highlight": {
        "font": ("Arial", 10),
        "foreground": colors['graphite'],
        "borderwidth": 1,
        "bordercolor": colors['green'],
    },
    "lbl-status": {
        "font": ("Arial", 8),
        "foreground": colors['muted'],
        "borderwidth": 0
    },
    "lbl-success": {
        "font": ("Arial", 10, "bold"),
        "foreground": colors['green'],
        "borderwidth": 0
    },
    "lbl-primary": {
        "font": ("Arial", 10),
        "foreground": colors['graphite'],
        "borderwidth": 0
    }
}

def init_styles(root):
    style = ttk.Style(root)

    style.configure("primary.TButton", **stylesheet["btn-primary"])
    style.configure("clear.TButton", **stylesheet["btn-clear"])
    style.configure("highlight.TButton", **stylesheet["btn-highlight"])
    style.configure("status.TLabel", **stylesheet["lbl-status"])
    style.configure("success.TLabel", **stylesheet["lbl-success"])
    style.configure("primary.TLabel", **stylesheet["lbl-primary"])

    return style

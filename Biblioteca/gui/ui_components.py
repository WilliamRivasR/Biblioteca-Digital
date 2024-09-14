import tkinter as tk
from tkinter import ttk

class NavigationBar:
    def __init__(self, parent, pages):
        self.parent = parent
        self.pages = pages
        self.frame = tk.Frame(parent, bg="#f0f0f0")
        self.buttons = {}
        self.create_widgets()

    def create_widgets(self):
        for page_name, page_obj in self.pages.items():
            if page_name not in ["login", "registration"]:
                btn = ttk.Button(self.frame, text=page_name.capitalize().replace("_", " "),
                                 command=lambda p=page_name: self.parent.show_frame(p))
                btn.pack(side=tk.LEFT, padx=5, pady=5)
                self.buttons[page_name] = btn

    def show_page(self, page_name):
        self.parent.show_frame(page_name)

    def pack(self):
        self.frame.pack(side=tk.TOP, fill=tk.X)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def grid_remove(self):
        self.frame.grid_remove()

class StatusBar:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bd=1, relief=tk.SUNKEN)
        self.label = tk.Label(self.frame, text="Ready")
        self.label.pack(side=tk.LEFT)

    def set_status(self, text):
        self.label.config(text=text)

    def pack(self):
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)

class CustomEntry(tk.Entry):
    def __init__(self, parent, placeholder, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ConfirmDialog:
    def __init__(self, parent, title, message):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        tk.Label(self.top, text=message).pack(pady=10)
        tk.Button(self.top, text="Yes", command=self.yes).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.top, text="No", command=self.no).pack(side=tk.RIGHT, padx=5, pady=5)
        self.top.protocol("WM_DELETE_WINDOW", self.no)
        self.top.transient(parent)
        self.top.grab_set()
        parent.wait_window(self.top)

    def yes(self):
        self.result = True
        self.top.destroy()

    def no(self):
        self.result = False
        self.top.destroy()
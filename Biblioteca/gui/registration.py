import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from database.database import DatabaseConnection

class RegistrationFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.db = DatabaseConnection()
        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0)

        self.frame = ttk.Frame(container, padding="20")
        self.frame.grid(row=0, column=0)

        style = ttk.Style()
        style.configure('TLabel', background='#f0f0f0')
        style.configure('TFrame', background='#f0f0f0')

        ttk.Label(self.frame, text="Registration", font=("Arial", 20)).grid(column=0, row=0, columnspan=2, pady=(0,20))

        self.fields = [
            ("User Type", ttk.Combobox(self.frame, values=['estudiante', 'directivo', 'docente', 'publico_general'], width=30)),
            ("Name", ttk.Entry(self.frame, width=30)),
            ("Surname", ttk.Entry(self.frame, width=30)),
            ("Birth Date", DateEntry(self.frame, date_pattern='yyyy-mm-dd', width=28)),
            ("Document Type", ttk.Combobox(self.frame, values=['CC', 'CE', 'PA', 'TI', 'PPT', 'PEP'], width=30)),
            ("Document Number", ttk.Entry(self.frame, width=30)),
            ("Email", ttk.Entry(self.frame, width=30)),
            ("Password", ttk.Entry(self.frame, show="*", width=30)),
            ("Phone", ttk.Entry(self.frame, width=30))
        ]

        for i, (text, entry) in enumerate(self.fields, start=1):
            ttk.Label(self.frame, text=text).grid(column=0, row=i, sticky=tk.W, pady=5)
            entry.grid(column=1, row=i, sticky=(tk.W, tk.E), pady=5)
            setattr(self, text.lower().replace(" ", "_"), entry)

        ttk.Button(self.frame, text="Register", command=self.register).grid(column=0, row=len(self.fields) + 1, columnspan=2, pady=(20,10))
        ttk.Button(self.frame, text="Back to Login", command=self.show_login).grid(column=0, row=len(self.fields) + 2, columnspan=2)

        self.message = ttk.Label(self.frame, text="")
        self.message.grid(column=0, row=len(self.fields) + 3, columnspan=2, pady=(10,0))

    def register(self):
        values = [getattr(self, field.lower().replace(" ", "_")).get() for field, _ in self.fields]
        cursor = self.db.call_procedure('InsertarUsuario', values)
        self.message.config(text="Registration successful! You can now login.")

    def show_login(self):
        self.master.show_frame("login")
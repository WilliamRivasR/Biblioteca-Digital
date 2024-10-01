import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from database.database import DatabaseConnection

class RegistrationFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#6287bf")  # Fondo principal azul
        self.master = master
        self.db = DatabaseConnection()
        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0)

        # Cambiar el color de fondo del frame principal a #2b4054
        self.frame = ttk.Frame(container, padding="20", style='Custom.TFrame')
        self.frame.grid(row=0, column=0)

        style = ttk.Style()
        style.configure('TLabel', background='#6287bf', foreground='#2b4054')  # Texto azul oscuro
        style.configure('Custom.TFrame', background='#2b4054')  # Fondo del frame oscuro
        style.configure('TButton', background='#2b4054', foreground='#2b4054')
        style.configure('TFrame', background='#6287bf')  # Fondo principal

        ttk.Label(self.frame, text="Registration", font=("Arial", 20), foreground='#2b4054').grid(column=0, row=0, columnspan=2, pady=(0, 20))

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

        ttk.Button(self.frame, text="Register", command=self.register).grid(column=0, row=len(self.fields) + 1, columnspan=2, pady=(20, 10))
        ttk.Button(self.frame, text="Back to Login", command=self.show_login).grid(column=0, row=len(self.fields) + 2, columnspan=2)

        self.message = ttk.Label(self.frame, text="", foreground="white")
        self.message.grid(column=0, row=len(self.fields) + 3, columnspan=2, pady=(10, 0))

    def register(self):
        # Resetear colores de fondo de los campos
        for field, entry in self.fields:
            entry.config(background="white")

        # Verificar que todos los campos estén llenos
        empty_fields = []
        values = []
        for field, entry in self.fields:
            value = entry.get()
            if not value:
                empty_fields.append((field, entry))
            values.append(value)

        if empty_fields:
            # Mostrar mensaje de error y resaltar los campos vacíos
            self.message.config(text="Please fill out all fields.", foreground="red")
            for field, entry in empty_fields:
                entry.config(background="#ffcccc")  # Fondo rojo para los campos vacíos
        else:
            # Registro exitoso
            cursor = self.db.call_procedure('InsertarUsuario', values)
            self.message.config(text="Registration successful! You can now login.", foreground="green")

    def show_login(self):
        self.master.show_frame("login")

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from database import DatabaseConnection

class RegistrationFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.db = DatabaseConnection()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        ttk.Label(self.scrollable_frame, text="Registration", font=("Arial", 20)).grid(column=0, row=0, columnspan=2, pady=20)

        # Definir los campos como un atributo de instancia
        self.fields = [
            ("User Type", ttk.Combobox(self.scrollable_frame, values=['estudiante', 'directivo', 'docente', 'publico_general'])),
            ("Name", ttk.Entry(self.scrollable_frame)),
            ("Surname", ttk.Entry(self.scrollable_frame)),
            ("Birth Date", DateEntry(self.scrollable_frame, date_pattern='yyyy-mm-dd')),
            ("Document Type", ttk.Combobox(self.scrollable_frame, values=['CC', 'CE', 'PA', 'TI', 'PPT', 'PEP'])),
            ("Document Number", ttk.Entry(self.scrollable_frame)),
            ("Email", ttk.Entry(self.scrollable_frame)),
            ("Password", ttk.Entry(self.scrollable_frame, show="*")),
            ("Phone", ttk.Entry(self.scrollable_frame))
        ]

        # Crear widgets para cada campo
        for i, (text, entry) in enumerate(self.fields, start=1):
            ttk.Label(self.scrollable_frame, text=text).grid(column=0, row=i, sticky=tk.W, pady=5)
            entry.grid(column=1, row=i, sticky=(tk.W, tk.E), pady=5)
            setattr(self, text.lower().replace(" ", "_"), entry)  # Añadir los widgets como atributos de la clase

        # Botones de registro y retorno al login
        ttk.Button(self.scrollable_frame, text="Register", command=self.register).grid(column=0, row=len(self.fields) + 1, columnspan=2, pady=20)
        ttk.Button(self.scrollable_frame, text="Back to Login", command=self.show_login).grid(column=0, row=len(self.fields) + 2, columnspan=2)

        self.message = ttk.Label(self.scrollable_frame, text="")
        self.message.grid(column=0, row=len(self.fields) + 3, columnspan=2, pady=10)

    def register(self):
        # Obtener todos los valores de los campos
        values = [getattr(self, field.lower().replace(" ", "_")).get() for field, _ in self.fields]

        # Llamar al procedimiento almacenado
        cursor = self.db.call_procedure('InsertarUsuario', values)

        self.message.config(text="Registration successful! You can now login.")

    def show_login(self):
        self.master.show_frame("login")

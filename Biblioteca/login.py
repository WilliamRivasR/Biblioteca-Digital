# login.py
import tkinter as tk
from tkinter import ttk
from database import DatabaseConnection

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.db = DatabaseConnection()
        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="Login", font=("Arial", 20)).grid(column=0, row=0, columnspan=2, pady=20)

        ttk.Label(self.frame, text="User Type:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.user_type = ttk.Combobox(self.frame, values=['estudiante', 'directivo', 'docente', 'publico_general'])
        self.user_type.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="Email:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.email = ttk.Entry(self.frame)
        self.email.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="Password:").grid(column=0, row=3, sticky=tk.W, pady=5)
        self.password = ttk.Entry(self.frame, show="*")
        self.password.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(self.frame, text="Login", command=self.login).grid(column=0, row=4, columnspan=2, pady=20)
        ttk.Button(self.frame, text="Register", command=self.show_register).grid(column=0, row=5, columnspan=2)

        self.message = ttk.Label(self.frame, text="")
        self.message.grid(column=0, row=6, columnspan=2, pady=10)

    def login(self):
        user_type = self.user_type.get()
        email = self.email.get().strip()
        password = self.password.get().strip()

        if not email or not password:
            self.message.config(text="Please enter email and password.")
            return

        try:
            with DatabaseConnection() as db:
                results = db.call_procedure('VerificarUsuario', [email, password, user_type])

                if results:
                    result = results[0]  # Obtén el primer resultado
                    if result[0] == 1:
                        self.message.config(text="Login successful!")
                        self.master.show_frame("usermanagement")
                    else:
                        self.message.config(text="Invalid email or password.")
                else:
                    self.message.config(text="No results returned from the procedure.")
        except Exception as e:
            self.message.config(text=f"An error occurred: {e}")

    def show_register(self):
        self.master.show_frame("registration")  # Asegúrate de que este nombre coincida con el nombre de la clave en create_frames

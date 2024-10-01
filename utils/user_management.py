import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database.database import DatabaseConnection
from PIL import Image, ImageTk

class UserManagementFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#6287bf")
        self.master = master
        self.db = DatabaseConnection()
        self.fields = [
            ("Document Number", ttk.Entry),
            ("Name", ttk.Entry),
            ("Surname", ttk.Entry),
            ("Birth Date", DateEntry),
            ("Email", ttk.Entry),
            ("Phone", ttk.Entry),
            ("Password", ttk.Entry)
        ]
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, padx=20, pady=20)

        # Cargar iconos de actualización y eliminación para las pestañas
        update_icon = ImageTk.PhotoImage(Image.open("F:/Biblioteca/icon/update_icon.png").resize((20, 20)))
        delete_icon = ImageTk.PhotoImage(Image.open("F:/Biblioteca/icon/delete_icon.png").resize((20, 20)))

        # Crear frames para las pestañas
        self.update_frame = ttk.Frame(self.notebook, style="Inner.TFrame", padding=10)
        self.delete_frame = ttk.Frame(self.notebook, style="Inner.TFrame", padding=10)

        # Agregar pestañas con iconos
        self.notebook.add(self.update_frame, text=" Update User", image=update_icon, compound=tk.LEFT)
        self.notebook.add(self.delete_frame, text=" Delete User", image=delete_icon, compound=tk.LEFT)

        # Mantener referencia a los iconos para que no se eliminen
        self.notebook.update_icon = update_icon
        self.notebook.delete_icon = delete_icon

        # Crear los widgets para cada frame
        self.create_update_widgets()
        self.create_delete_widgets()

    def create_update_widgets(self):
        update_inner_frame = ttk.Frame(self.update_frame, padding="20", style="Inner.TFrame")
        update_inner_frame.pack(expand=True)

        ttk.Label(update_inner_frame, text="Document Number:", background="#2b4054", foreground="white").grid(
            column=0, row=0, sticky=tk.W, pady=5)
        self.load_document_number = ttk.Entry(update_inner_frame)
        self.load_document_number.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(update_inner_frame, text="Password:", background="#2b4054", foreground="white").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.load_password = ttk.Entry(update_inner_frame, show="*")
        self.load_password.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(update_inner_frame, text="Load User Info", command=self.load_user_info).grid(column=0, row=2, columnspan=2, pady=10)

        for i, (text, entry_type) in enumerate(self.fields):
            ttk.Label(update_inner_frame, text=text, background="#2b4054", foreground="white").grid(column=0, row=i + 3, sticky=tk.W, pady=5)
            if entry_type == DateEntry:
                entry = entry_type(update_inner_frame, date_pattern='yyyy-mm-dd')
            elif text == "Password":
                entry = entry_type(update_inner_frame, show="*")
            else:
                entry = entry_type(update_inner_frame)
            entry.grid(column=1, row=i + 3, sticky=(tk.W, tk.E), pady=5)
            setattr(self, f"update_{text.lower().replace(' ', '_')}", entry)

        update_button = ttk.Button(update_inner_frame, text="Update User", command=self.update_user)
        update_button.grid(column=0, row=len(self.fields) + 3, columnspan=2, pady=20)

        self.update_message = ttk.Label(update_inner_frame, text="", background="#2b4054", foreground="white")
        self.update_message.grid(column=0, row=len(self.fields) + 4, columnspan=2, pady=10)

    def create_delete_widgets(self):
        delete_inner_frame = ttk.Frame(self.delete_frame, padding="20", style="Inner.TFrame")
        delete_inner_frame.pack(expand=True)

        ttk.Label(delete_inner_frame, text="Document Number:", background="#2b4054", foreground="white").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.delete_document_number = ttk.Entry(delete_inner_frame)
        self.delete_document_number.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(delete_inner_frame, text="Password:", background="#2b4054", foreground="white").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.delete_password = ttk.Entry(delete_inner_frame, show="*")
        self.delete_password.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

        delete_button = ttk.Button(delete_inner_frame, text="Delete User", command=self.delete_user)
        delete_button.grid(column=0, row=2, columnspan=2, pady=20)

        self.delete_message = ttk.Label(delete_inner_frame, text="", background="#2b4054", foreground="white")
        self.delete_message.grid(column=0, row=3, columnspan=2, pady=10)


    def load_user_info(self):
        document_number = self.load_document_number.get()
        password = self.load_password.get()

        if not document_number or not password:
            messagebox.showerror("Error", "Please enter both document number and password.")
            return

        query = "SELECT Nombre, Apellidos, Fecha_nacimiento, Correo_electronico, Telefono, Contraseña FROM usuarios WHERE Numero_documento = %s"
        with DatabaseConnection() as db:
            try:
                db.cursor.execute(query, (document_number,))
                result = db.cursor.fetchone()

                if result:
                    stored_password = result[5]
                    if stored_password != password:
                        messagebox.showerror("Error", "Incorrect password.")
                        return

                    self.update_name.delete(0, tk.END)
                    self.update_name.insert(0, result[0])

                    self.update_surname.delete(0, tk.END)
                    self.update_surname.insert(0, result[1])

                    self.update_birth_date.set_date(result[2])

                    self.update_email.delete(0, tk.END)
                    self.update_email.insert(0, result[3])

                    self.update_phone.delete(0, tk.END)
                    self.update_phone.insert(0, result[4])

                    self.update_message.config(text="User info loaded successfully.", foreground="green")
                else:
                    messagebox.showerror("Error", "User not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load user info: {str(e)}")

    def update_user(self):
        values = [getattr(self, f"update_{field[0].lower().replace(' ', '_')}").get() for field in self.fields]
        query = "UPDATE usuarios SET Nombre=%s, Apellidos=%s, Fecha_nacimiento=%s, Correo_electronico=%s, Telefono=%s, Contraseña=%s WHERE Numero_documento=%s"
        with DatabaseConnection() as db:
            try:
                db.cursor.execute(query, (*values, self.load_document_number.get()))
                db.connection.commit()
                messagebox.showinfo("Success", "User updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update user: {str(e)}")

    def delete_user(self):
        document_number = self.delete_document_number.get()
        password = self.delete_password.get()

        if not document_number or not password:
            messagebox.showerror("Error", "Please enter both document number and password.")
            return

        query = "SELECT Contraseña FROM usuarios WHERE Numero_documento = %s"
        with DatabaseConnection() as db:
            try:
                db.cursor.execute(query, (document_number,))
                result = db.cursor.fetchone()

                if result:
                    stored_password = result[0]
                    if stored_password != password:
                        messagebox.showerror("Error", "Incorrect password.")
                        return

                    delete_query = "DELETE FROM usuarios WHERE Numero_documento = %s"
                    db.cursor.execute(delete_query, (document_number,))
                    db.connection.commit()
                    messagebox.showinfo("Success", "User deleted successfully!")
                else:
                    messagebox.showerror("Error", "User not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")


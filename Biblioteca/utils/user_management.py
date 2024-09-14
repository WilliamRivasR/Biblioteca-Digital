import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database.database import DatabaseConnection

class UserManagementFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
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

        self.update_frame = ttk.Frame(self.notebook)
        self.delete_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.update_frame, text="Update User")
        self.notebook.add(self.delete_frame, text="Delete User")

        self.create_update_widgets()
        self.create_delete_widgets()

    def create_update_widgets(self):
        update_inner_frame = ttk.Frame(self.update_frame, padding="20")
        update_inner_frame.pack(expand=True)

        for i, (text, entry_type) in enumerate(self.fields):
            ttk.Label(update_inner_frame, text=text).grid(column=0, row=i, sticky=tk.W, pady=5)
            if entry_type == DateEntry:
                entry = entry_type(update_inner_frame, date_pattern='yyyy-mm-dd')
            elif text == "Password":
                entry = entry_type(update_inner_frame, show="*")
            else:
                entry = entry_type(update_inner_frame)
            entry.grid(column=1, row=i, sticky=(tk.W, tk.E), pady=5)
            setattr(self, f"update_{text.lower().replace(' ', '_')}", entry)

        ttk.Button(update_inner_frame, text="Update User", command=self.update_user).grid(column=0, row=len(self.fields), columnspan=2, pady=20)

        self.update_message = ttk.Label(update_inner_frame, text="")
        self.update_message.grid(column=0, row=len(self.fields)+1, columnspan=2, pady=10)

    def create_delete_widgets(self):
        delete_inner_frame = ttk.Frame(self.delete_frame, padding="20")
        delete_inner_frame.pack(expand=True)

        ttk.Label(delete_inner_frame, text="Document Number:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.delete_document_number = ttk.Entry(delete_inner_frame)
        self.delete_document_number.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(delete_inner_frame, text="Delete User", command=self.delete_user).grid(column=0, row=1, columnspan=2, pady=20)

        self.delete_message = ttk.Label(delete_inner_frame, text="")
        self.delete_message.grid(column=0, row=2, columnspan=2, pady=10)

    def update_user(self):
        values = [getattr(self, f"update_{field[0].lower().replace(' ', '_')}").get() for field in self.fields]
        result = self.db.call_procedure('ActualizarUsuario', values)
        if result:
            messagebox.showinfo("Success", "User updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update user.")

    def delete_user(self):
        document_number = self.delete_document_number.get()
        result = self.db.call_procedure('BorrarUsuario', [document_number])
        if result:
            messagebox.showinfo("Success", "User deleted successfully!")
        else:
            messagebox.showerror("Error", "Failed to delete user.")
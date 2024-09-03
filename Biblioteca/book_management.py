import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection

class BookManagementFrame(tk.Frame):  # Cambiar para heredar de tk.Frame
    def __init__(self, parent):
        super().__init__(parent)  # Llama al constructor de la clase base tk.Frame
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self, text="Book Management", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Add Book Section
        add_book_frame = tk.LabelFrame(self, text="Add New Book")
        add_book_frame.pack(padx=10, pady=10, fill="x")

        labels = ["Title:", "Author:", "Publication Year:", "Genre:", "Summary:", "Available Copies:", "Status:"]
        self.entries = {}

        for label in labels:
            tk.Label(add_book_frame, text=label).pack()
            if label == "Publication Year:":
                self.entries[label] = tk.Spinbox(add_book_frame, from_=1900, to=2100, format="%04.0f", width=5)
            else:
                self.entries[label] = tk.Entry(add_book_frame)
            self.entries[label].pack(pady=5)

        tk.Button(add_book_frame, text="Add Book", command=self.add_book).pack(pady=10)

        # Show Available Books Section
        tk.Button(self, text="Show Available Books", command=self.show_available_books).pack(pady=10)

        # Treeview for displaying books
        self.tree = ttk.Treeview(self,
                                 columns=("ID", "Title", "Author", "Year", "Genre", "Summary", "Copies", "Status"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10, fill="both", expand=True)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def add_book(self):
        book_data = {label.rstrip(':'): entry.get() for label, entry in self.entries.items()}

        with DatabaseConnection() as db:
            try:
                result = db.call_procedure('AgregarLibro', list(book_data.values()))
                if result is not None:
                    messagebox.showinfo("Success", "Book added successfully!")
                    for entry in self.entries.values():
                        entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Failed to add book.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book: {str(e)}")

    def show_available_books(self):
        with DatabaseConnection() as db:
            try:
                result = db.call_procedure('ObtenerLibrosDisponibles')
                self.tree.delete(*self.tree.get_children())
                if result:
                    for book in result:
                        self.tree.insert("", "end", values=book)
                else:
                    messagebox.showinfo("Info", "No available books found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch books: {str(e)}")


    def pack(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
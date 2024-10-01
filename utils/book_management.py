import tkinter as tk
from tkinter import ttk, messagebox
from database.database import DatabaseConnection


class BookManagementFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.configure(bg="#6287bf")  # Fondo principal


    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20", style='Main.TFrame')  # Fondo principal
        main_frame.pack(expand=True, fill="both")

        # Configurar el estilo para usar el color de fondo
        style = ttk.Style()
        style.configure('Main.TFrame', background='#6287bf')
        style.configure('TFrame', background='#2b4054')
        style.configure('TLabel', background='#6287bf', foreground="black")
        style.configure('TLabelframe', background='#2b4054', foreground="black")
        style.configure('TLabelframe.Label', background='#2b4054', foreground="black")
        style.configure('TButton', background='#2b4054', foreground="black")

        # Title
        title = tk.Label(main_frame, text="Book Management", font=("Arial", 16, "bold"), bg="#6287bf", fg="white")
        title.pack(pady=10)

        # Content frame
        content_frame = ttk.Frame(main_frame, style='TFrame')
        content_frame.pack(expand=True, fill="both")

        # Left frame for Add Book and Treeview
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True)

        # Add Book Section
        add_book_frame = ttk.LabelFrame(left_frame, text="Add New Book", padding="10", style='TLabelframe')
        add_book_frame.pack(padx=10, pady=10, fill="x")

        # Center the input fields
        add_book_frame.grid_columnconfigure(0, weight=1)
        add_book_frame.grid_columnconfigure(2, weight=1)

        labels = ["Title:", "Author:", "Publication Year:", "Genre:", "Summary:", "Available Copies:", "Status:"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(add_book_frame, text=label).grid(row=i, column=1, sticky="e", padx=(0, 5), pady=5)
            if label == "Publication Year:":
                self.entries[label] = ttk.Spinbox(add_book_frame, from_=1900, to=2100, format="%04.0f", width=40)
            elif label == "Summary:":
                self.entries[label] = tk.Text(add_book_frame, height=3, width=40, bg="#ffffff", fg="black")
            else:
                self.entries[label] = ttk.Entry(add_book_frame, width=40)
            self.entries[label].grid(row=i, column=2, sticky="w", pady=5)

        # Botón para agregar libro
        ttk.Button(add_book_frame, text="Add Book", command=self.add_book).grid(row=len(labels), column=1, columnspan=2,
                                                                                pady=10)

        add_book_frame.grid_columnconfigure(0, weight=1)
        add_book_frame.grid_columnconfigure(1, weight=1)

        # Show Available Books Section
        ttk.Button(left_frame, text="Show Available Books", command=self.show_available_books).pack(pady=10)

        # Treeview for displaying books
        self.tree = ttk.Treeview(left_frame,
                                 columns=("ID", "Title", "Author", "Year", "Genre", "Summary", "Copies", "Status"),
                                 show="headings", height=10)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10, fill="both", expand=True)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind the TreeviewSelect event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Right frame for book details
        self.right_frame = ttk.Frame(content_frame, padding="20", style='TFrame')
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Labels for book details
        self.book_title_label = ttk.Label(self.right_frame, text="", font=("Arial", 14, "bold"), wraplength=300)
        self.book_title_label.pack(pady=(0, 10))

        self.book_summary_label = ttk.Label(self.right_frame, text="", wraplength=300, justify="left")
        self.book_summary_label.pack(pady=10)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        book = self.tree.item(selected_item)
        title = book['values'][1]  # Título es la segunda columna
        summary = book['values'][5]  # Resumen es la sexta columna

        # Actualizar las etiquetas con la información del libro seleccionado
        self.book_title_label.config(text=title)
        self.book_summary_label.config(text=summary)

    def add_book(self):
        # Diccionario para almacenar los datos del libro
        book_data = {}

        # Iterar sobre las entradas del formulario
        for label, entry in self.entries.items():
            # Obtener el valor del campo
            value = entry.get() if not isinstance(entry, tk.Text) else entry.get("1.0", tk.END).strip()

            # Validación para el campo 'Publication Year' que no debe estar vacío
            if label == "Publication Year:":
                if value == '':
                    book_data[label.rstrip(':')] = None  # Convertir a NULL si está vacío
                else:
                    book_data[label.rstrip(':')] = int(value)  # Convertir a entero
            else:
                book_data[label.rstrip(':')] = value

        # Conexión a la base de datos
        with DatabaseConnection() as db:
            try:
                # Insertar el libro y obtener el ID del libro recién insertado
                result = db.call_procedure(proc_name='AgregarLibro', params=list(book_data.values()))

                if result is not None:
                    # Mostrar mensaje de éxito
                    messagebox.showinfo(title="Success", message="Book added successfully!")

                    # Limpiar el formulario
                    for entry in self.entries.values():
                        if isinstance(entry, tk.Text):
                            entry.delete("1.0", tk.END)
                        else:
                            entry.delete(0, tk.END)

                else:
                    # Mostrar mensaje de error si no se pudo insertar el libro
                    messagebox.showerror(title="Error", message="Failed to add book.")

            except Exception as e:
                # Mostrar mensaje de error con la excepción
                messagebox.showerror("Error", message=f"Failed to add book: {str(e)}")

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
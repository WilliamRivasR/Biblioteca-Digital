import tkinter as tk
from tkinter import ttk, messagebox
from database.database import DatabaseConnection
from PIL import Image, ImageTk
import tkinter.filedialog as fd


class BookManagementFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.image_path = None  # Variable para almacenar la ruta de la imagen
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Title
        title = tk.Label(main_frame, text="Book Management", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(expand=True, fill="both")

        # Add Book Section
        add_book_frame = ttk.LabelFrame(content_frame, text="Add New Book", padding="10")
        add_book_frame.pack(side="left", padx=10, pady=10, fill="y")

        labels = ["Title:", "Author:", "Publication Year:", "Genre:", "Summary:", "Available Copies:", "Status:"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(add_book_frame, text=label).grid(row=i, column=0, sticky="e", padx=(0, 5), pady=5)
            if label == "Publication Year:":
                self.entries[label] = ttk.Spinbox(add_book_frame, from_=1900, to=2100, format="%04.0f", width=20)
            elif label == "Summary:":
                self.entries[label] = tk.Text(add_book_frame, height=3, width=40)
            else:
                self.entries[label] = ttk.Entry(add_book_frame, width=40)
            self.entries[label].grid(row=i, column=1, sticky="w", pady=5)

        # Botón para seleccionar imagen
        ttk.Button(add_book_frame, text="Upload Book Image", command=self.upload_image).grid(row=len(labels), column=0,
                                                                                             columnspan=2, pady=10)

        # Botón para agregar libro
        ttk.Button(add_book_frame, text="Add Book", command=self.add_book).grid(row=len(labels) + 1, column=0,
                                                                                columnspan=2, pady=10)

        # Image display
        image_frame = ttk.Frame(content_frame)
        image_frame.pack(side="right", padx=10, pady=10)

        self.image_label = ttk.Label(image_frame)
        self.image_label.pack()

        self.load_image(1)  # Load image with ID 1

        # Show Available Books Section
        ttk.Button(main_frame, text="Show Available Books", command=self.show_available_books).pack(pady=10)

        # Treeview for displaying books
        self.tree = ttk.Treeview(main_frame,
                                 columns=("ID", "Title", "Author", "Year", "Genre", "Summary", "Copies", "Status"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10, fill="both", expand=True)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def upload_image(self):
        # Abrir diálogo para seleccionar imagen
        file_path = fd.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.image_path = file_path  # Guardar la ruta de la imagen
            image = Image.open(file_path)
            image = image.resize((200, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

    def add_book(self):
        # Obtener los datos del formulario
        book_data = {}
        for label, entry in self.entries.items():
            value = entry.get() if not isinstance(entry, tk.Text) else entry.get("1.0", tk.END).strip()

            # Validación para el campo 'Publication Year' que no debe estar vacío
            if label == "Publication Year:":
                if value == '':
                    book_data[label.rstrip(':')] = None  # Convertir a NULL si está vacío
                else:
                    book_data[label.rstrip(':')] = int(value)  # Convertir a entero
            else:
                book_data[label.rstrip(':')] = value

        with DatabaseConnection() as db:
            try:
                # Insertar el libro y obtener el ID del libro recién insertado
                result = db.call_procedure('AgregarLibro', list(book_data.values()))

                if result is not None:
                    libro_id = result[0][0]  # Obtener el ID del libro recién insertado

                    # Si hay una imagen cargada, insertarla en la tabla imagenes
                    if self.image_path:
                        self.insert_image_into_db(libro_id, self.image_path)
                    messagebox.showinfo("Success", "Book and image added successfully!")

                    # Limpiar el formulario
                    for entry in self.entries.values():
                        if isinstance(entry, tk.Text):
                            entry.delete("1.0", tk.END)
                        else:
                            entry.delete(0, tk.END)
                    self.image_label.configure(image=None)  # Limpiar la imagen
                    self.image_path = None  # Resetear la ruta de la imagen
                else:
                    messagebox.showerror("Error", "Failed to add book.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book: {str(e)}")

    def insert_image_into_db(self, libro_id, image_path):
        image_name = image_path.split("/")[-1]  # Extraer el nombre del archivo de la ruta
        with DatabaseConnection() as db:
            try:
                # Insertar la imagen en la tabla imagenes con el libro_id
                db.call_procedure('AgregarImagen', [libro_id, image_name, image_path])
                messagebox.showinfo("Éxito", "Imagen subida con éxito!")
            except Exception as e:
                messagebox.showerror("Error", f"Error al subir imagen: {str(e)}")

    def load_image(self, image_id):
        with DatabaseConnection() as db:
            try:
                result = db.call_procedure('ObtenerUbicacionImagen', [image_id])
                if result:
                    image_path = result[0][0]
                    image = Image.open(image_path)
                    image = image.resize((200, 300), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.image_label.configure(image=photo)
                    self.image_label.image = photo
            except Exception as e:
                print(f"Failed to load image: {str(e)}")

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



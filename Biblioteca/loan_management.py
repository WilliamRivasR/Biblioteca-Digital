import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import DatabaseConnection

class LoanManagementFrame(tk.Frame):  # Cambiar para heredar de tk.Frame
    def __init__(self, parent):
        super().__init__(parent)  # Llama al constructor de la clase base tk.Frame
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self, text="Loan Management", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Loan Book Section
        loan_frame = tk.LabelFrame(self, text="Loan a Book")
        loan_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(loan_frame, text="Book ID:").pack()
        self.book_id_entry = tk.Entry(loan_frame)
        self.book_id_entry.pack(pady=5)

        tk.Label(loan_frame, text="Loan Date:").pack()
        self.loan_date_entry = DateEntry(loan_frame, date_pattern='yyyy-mm-dd')
        self.loan_date_entry.pack(pady=5)

        tk.Button(loan_frame, text="Loan Book", command=self.loan_book).pack(pady=10)

        # Show Loans Section
        tk.Button(self, text="Show All Loans", command=self.show_loans).pack(pady=10)

        # Treeview for displaying loans
        self.tree = ttk.Treeview(self, columns=("Loan ID", "Book Name", "User ID", "Loan Date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10, fill="both", expand=True)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Return Book Section
        return_frame = tk.LabelFrame(self, text="Return a Book")
        return_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(return_frame, text="Loan ID:").pack()
        self.return_loan_id_entry = tk.Entry(return_frame)
        self.return_loan_id_entry.pack(pady=5)

        tk.Button(return_frame, text="Return Book", command=self.return_book).pack(pady=10)

    def loan_book(self):
        book_id = self.book_id_entry.get()
        loan_date = self.loan_date_entry.get()
        user_id = "current_user_id"  # Esto debería obtenerse del usuario actualmente conectado

        with DatabaseConnection() as db:
            try:
                result = db.call_procedure('AgregarLibroPrestado', [user_id, book_id, loan_date])
                if result is not None:
                    messagebox.showinfo("Success", "Book loaned successfully!")
                    self.book_id_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Failed to loan book.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to loan book: {str(e)}")

    def show_loans(self):
        with DatabaseConnection() as db:
            try:
                # Ejecutar la consulta SQL directamente para obtener todos los préstamos
                db.cursor.execute('SELECT * FROM prestamos')  # Usar el cursor para ejecutar la consulta
                result = db.cursor.fetchall()  # Obtener todos los resultados

                # Limpiar el Treeview antes de insertar nuevos datos
                self.tree.delete(*self.tree.get_children())

                if result:
                    # Insertar cada préstamo en el Treeview
                    for loan in result:
                        self.tree.insert("", "end", values=loan)
                else:
                    messagebox.showinfo("Info", "No se encontraron préstamos.")

            except Exception as e:
                messagebox.showerror("Error", f"Error al obtener los préstamos: {str(e)}")

    def return_book(self):
        loan_id = self.return_loan_id_entry.get()  # Obtener el ID del préstamo desde la entrada

        with DatabaseConnection() as db:
            try:
                # Ejecutar la consulta SQL para eliminar el préstamo por su ID
                db.cursor.execute('DELETE FROM prestamos WHERE ID_prestamo = %s', (loan_id,))  # Consulta SQL para eliminar
                db.connection.commit()  # Confirmar los cambios en la base de datos

                # Verificar si se eliminó algún registro
                if db.cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Book returned successfully!")
                    self.return_loan_id_entry.delete(0, tk.END)  # Limpiar la entrada
                    self.show_loans()  # Actualizar la lista de préstamos
                else:
                    messagebox.showerror("Error", "Failed to return book. No matching loan found.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def pack(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
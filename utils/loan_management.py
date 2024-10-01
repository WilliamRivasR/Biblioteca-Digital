import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database.database import DatabaseConnection

class LoanManagementFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#6287bf")
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self, padding="20", style="Main.TFrame")
        main_frame.pack(expand=True, fill="both")

        # Title
        title = tk.Label(main_frame, text="Loan Management", font=("Arial", 16, "bold"), bg="#6287bf", fg="white")
        title.pack(pady=10)

        # Create and Delete Loan Section
        create_delete_loan_frame = ttk.Frame(main_frame, padding="10", borderwidth=1, relief="solid", style="Inner.TFrame")
        create_delete_loan_frame.pack(padx=10, pady=10, fill="x")

        loan_delete_frame = ttk.Frame(create_delete_loan_frame, padding="10", style="Inner.TFrame")
        loan_delete_frame.pack(fill="both", expand=True)

        # Loan Book Section
        loan_frame = ttk.Frame(loan_delete_frame, padding="10", style="Inner.TFrame")
        loan_frame.pack(side="left", padx=10, pady=10, fill="y")

        ttk.Label(loan_frame, text="Book ID:", background="#2b4054", foreground="white").pack()
        self.book_id_entry = ttk.Entry(loan_frame, validate="key", validatecommand=(self.register(self.validate_number), '%P'))
        self.book_id_entry.pack(pady=5)

        ttk.Label(loan_frame, text="Loan Date:", background="#2b4054", foreground="white").pack()
        self.loan_date_entry = DateEntry(loan_frame, date_pattern='yyyy-mm-dd')
        self.loan_date_entry.pack(pady=5)

        ttk.Button(loan_frame, text="Loan Book", command=self.loan_book).pack(pady=10)

        # Delete Loan Section
        delete_loan_frame = ttk.Frame(loan_delete_frame, padding="10", style="Inner.TFrame")
        delete_loan_frame.pack(side="right", padx=10, pady=10, fill="y")

        ttk.Label(delete_loan_frame, text="Loan ID:", background="#2b4054", foreground="white").pack()
        self.delete_loan_id_entry = ttk.Entry(delete_loan_frame, validate="key", validatecommand=(self.register(self.validate_number), '%P'))
        self.delete_loan_id_entry.pack(pady=5)

        ttk.Button(delete_loan_frame, text="Delete Loan", command=self.delete_loan).pack(pady=10)

        # Show Loans Section
        ttk.Button(main_frame, text="Show All Loans", command=self.show_loans).pack(pady=10)

        # Treeview for displaying loans
        self.tree = ttk.Treeview(main_frame, columns=("Loan ID", "Book Name", "User ID", "Loan Date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10, fill="both", expand=True)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Return Book Section
        return_frame = ttk.LabelFrame(main_frame, text="Return a Book", padding="10", style="Inner.TFrame")
        return_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(return_frame, text="Loan ID:", background="#2b4054", foreground="white").pack()
        self.return_loan_id_entry = ttk.Entry(return_frame, validate="key", validatecommand=(self.register(self.validate_number), '%P'))
        self.return_loan_id_entry.pack(pady=5)

        ttk.Button(return_frame, text="Return Book", command=self.return_book).pack(pady=10)

    def validate_number(self, P):
        return P.isdigit() or P == ""

    def loan_book(self):
        book_id = self.book_id_entry.get()
        loan_date = self.loan_date_entry.get()
        user_id = "5962225"  # Esto debería obtenerse del usuario actualmente conectado

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

    def delete_loan(self):
        loan_id = self.delete_loan_id_entry.get()
        if loan_id.isdigit():
            with DatabaseConnection() as db:
                try:
                    db.cursor.execute('DELETE FROM prestamos WHERE ID_prestamo = %s', (loan_id,))
                    db.connection.commit()
                    if db.cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Loan deleted successfully!")
                        self.delete_loan_id_entry.delete(0, tk.END)
                        self.show_loans()
                    else:
                        messagebox.showerror("Error", "Failed to delete loan. No matching loan found.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete loan: {str(e)}")
        else:
            messagebox.showerror("Error", "Error: The loan ID is not correct")

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
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from login import LoginFrame
from registration import RegistrationFrame
from utils.user_management import UserManagementFrame
from utils.book_management import BookManagementFrame
from utils.loan_management import LoanManagementFrame

class NavigationBar:
    def __init__(self, parent, frames):
        self.parent = parent
        self.frames = frames
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        # Load icons
        user_icon = ImageTk.PhotoImage(Image.open("F:/Biblioteca/icon/user_management_icon.png").resize((20, 20)))
        book_icon = ImageTk.PhotoImage(Image.open("F:/Biblioteca/icon/book_management_icon.png").resize((20, 20)))
        loan_icon = ImageTk.PhotoImage(Image.open("F:/Biblioteca/icon/loan_management_icon.png").resize((20, 20)))

        self.user_management_button = ttk.Button(
            self.frame,
            text="User Management",
            image=user_icon,
            compound=tk.LEFT,
            command=lambda: self.parent.show_frame("usermanagement")
        )
        self.user_management_button.pack(side=tk.LEFT, padx=5)
        self.user_management_button.image = user_icon

        self.book_management_button = ttk.Button(
            self.frame,
            text="Book Management",
            image=book_icon,
            compound=tk.LEFT,
            command=lambda: self.parent.show_frame("bookmanagement")
        )
        self.book_management_button.pack(side=tk.LEFT, padx=5)
        self.book_management_button.image = book_icon

        self.loan_management_button = ttk.Button(
            self.frame,
            text="Loan Management",
            image=loan_icon,
            compound=tk.LEFT,
            command=lambda: self.parent.show_frame("loanmanagement")
        )
        self.loan_management_button.pack(side=tk.LEFT, padx=5)
        self.loan_management_button.image = loan_icon

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca Escolar")
        self.iconbitmap("F:\Biblioteca\icon\Icono.ico")
        self.geometry("800x600")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_frames()
        self.create_menu()
        self.create_navigation_bar()

        self.show_frame("login")

    def create_frames(self):
        self.frames = {}
        for F in (LoginFrame, RegistrationFrame, UserManagementFrame, BookManagementFrame, LoanManagementFrame):
            frame = F(self)
            frame_name = F.__name__.lower().replace("frame", "")
            self.frames[frame_name] = frame
            frame.grid(row=1, column=0, sticky="nsew")
            frame.grid_remove()

    def create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def create_navigation_bar(self):
        self.nav_bar = NavigationBar(self, self.frames)
        self.nav_bar.frame.grid(row=0, column=0, sticky="ew")

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[frame_name]
        frame.grid(row=1, column=0, sticky="nsew")

        if frame_name in ["login", "registration"]:
            self.nav_bar.frame.grid_remove()
            self.geometry("800x600")
        elif frame_name == "usermanagement":
            self.nav_bar.frame.grid(row=0, column=0, sticky="ew")
            self.geometry("430x600")
        elif frame_name == "bookmanagement":
            self.nav_bar.frame.grid(row=0, column=0, sticky="ew")
            self.geometry("1200x800")
        else:
            self.nav_bar.frame.grid(row=0, column=0, sticky="ew")
            self.geometry("800x600")

    def logout(self):
        self.show_frame("login")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
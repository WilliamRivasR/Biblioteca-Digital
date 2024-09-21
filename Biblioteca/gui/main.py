import tkinter as tk
from tkinter import ttk
from login import LoginFrame
from registration import RegistrationFrame
from utils.user_management import UserManagementFrame
from utils.book_management import BookManagementFrame
from utils.loan_management import LoanManagementFrame
from ui_components import NavigationBar

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Biblioteca Escolar")
        self.geometry("800x600")
        self.resizable(False, False)  # Allow window resizing
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
            self.geometry("800x600")  # Reset to default size for login/registration
        else:
            self.nav_bar.frame.grid(row=0, column=0, sticky="ew")
            if frame_name == "bookmanagement":
                self.geometry("1200x800")  # Set larger size for book management
            else:
                self.geometry("800x600")  # Reset to default size for other frames

    def logout(self):
        self.show_frame("login")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
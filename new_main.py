import tkinter as tk
from GUI.mainapp import MainApp
from GUI.login_page import LoginPage


if __name__ == "__main__":
    mainapp = MainApp()
    login_page = LoginPage(mainapp)
    mainapp.mainloop()

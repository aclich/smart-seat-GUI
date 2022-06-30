import tkinter as tk

class BasePage(tk.Frame):
    def __init__(self, mainframe: tk.Frame, mainapp:tk.Tk):
        tk.Frame.__init__(self, mainframe)
        self.mainapp = mainapp

        self.page_geometry = '200x200+300+150'
        self.page_title = 'defult page'
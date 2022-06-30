import tkinter as tk
from GUI.Basepage import BasePage

class SensorFrame(tk.Frame):
    def __init__(self, page: BasePage, mainapp):
        tk.Frame().__init__(page)

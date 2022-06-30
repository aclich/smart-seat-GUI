import tkinter as tk
from tkinter import messagebox
from libs.http_request import backend_connenct
from libs.sensor.serial_port import Sensor_Board
from libs.sitpos_predict.classifier import classifier
from GUI.login_page import LoginPage
# FONT = Font(family='微軟正黑體', size=12)
from GUI.Basepage import BasePage
from GUI.user_page import UserPage

PageList = [UserPage]

class MainApp(tk.Tk):
    def __init__(self, title="smart_seat", geometry='1200x700+150+0'):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.iconbitmap('GUI/img/cushions.ico')
        self.connector = backend_connenct(self)
        self.classifer = classifier()
        
        self.mainframe = tk.Frame()
        self.mainframe.grid(row=0, column=0, sticky='nesw')

        self._init_pages()
    
    def _init_pages(self):
        self.pages = {}
        for page in PageList:
            p = page(mainframe=self.mainframe, mainapp=self)
            p.grid(row=0, column=0, sticky='nswe')
            self.pages[page.__name__] = p
        
    def change_page(self, page_name):
        if page_name not in self.pages:
            messagebox.showerror(f"找不到指定頁面:{page_name}")
            return
        page: BasePage = self.pages[page_name]
        self.geometry(page.page_geometry)
        page._Layout()
        page.tkraise()
        
        
    def login(self):
        print('main login')
        self.change_page('UserPage')
        pass


        
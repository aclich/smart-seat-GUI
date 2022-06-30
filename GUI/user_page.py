import tkinter as tk
from GUI.Basepage import BasePage

class UserPage(BasePage):
    def __init__(self, mainframe:tk.Frame, mainapp:tk.Tk):
        super().__init__(mainframe, mainapp)

        self.page_geometry = '1200x700+150+0'
        self.page_title = 'User window'
        self._create_component()
        self._Layout()

    def _create_component(self):    
        self.label1 = tk.Label(self, text=f'Login:{self.mainapp.connector.login_status}')


    def _Layout(self):
        self.label1.grid()

        self.update()
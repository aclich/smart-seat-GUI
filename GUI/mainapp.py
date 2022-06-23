import tkinter as tk
from libs.http_request import backend_connenct
from libs.sensor.serial_port import Sensor_Board
from libs.sitpos_predict.classifier import classifier
from GUI.login_page import LoginPage
# FONT = Font(family='微軟正黑體', size=12)



class MainApp(tk.Tk):
    def __init__(self, title="smart_seat", geometry='450x300+300+100'):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.connector = backend_connenct(self)
        self.classifer = classifier()
        self.mainframe = tk.Frame()

        self.mainframe.pack(side='top', fill='both', expand=True)

    

    
    def login(self):
        print('main login')
        self.geometry('700x800')
        self.label = tk.Label(self, text=f'{self.connector.login_status}')
        self.label.pack()
        self.update()
        pass

        
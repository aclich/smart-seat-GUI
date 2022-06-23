import tkinter as tk
from tkinter import messagebox
from libs.config import SA_EMAIL, SA_PWD
from GUI.pop_out import BasePopOut
from libs.http_request import backend_connenct

class LoginPage(BasePopOut):
    def __init__(self, mainapp: tk.Tk):
        super().__init__(mainapp)
        self.mainapp = mainapp
        # self.mainapp.withdraw()  #隱藏主視窗
        
        self.title('Login')
        self.geometry('450x300+300+100')
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._create_component()
        self._Layout()
        
        self.update()

    def _create_component(self):
        self.img_file = tk.PhotoImage(file=r"GUI/img/welcome.gif")
        self.logo_cav = tk.Canvas(self, height=200, width=500)
        self.logo_cav.create_image(0, 0, image=self.img_file, anchor='nw')
        
        self.lb1 = tk.Label(self, text="User emal : ")
        self.lb2 = tk.Label(self, text='Password : ')

        self.email_var = tk.StringVar(value=SA_EMAIL)
        self.password_var = tk.StringVar(value=SA_PWD)
        self.email_entry = tk.Entry(self, textvariable=self.email_var)
        self.pwd_entry = tk.Entry(self, textvariable=self.password_var, show='*')

        self.btn_login = tk.Button(self, text='Login', command=self._login_web)
        self.btn_sign_up = tk.Button(self, text='Sign Up', command=lambda: None)
        self.btn_sign_up['command'] = lambda: print("config lambda sign up")

    def _Layout(self):
        self.logo_cav.pack(side=tk.TOP)
        self.lb1.place(x=50, y=150)
        self.lb2.place(x=50, y=190)
        self.email_entry.place(x=130, y=150)
        self.pwd_entry.place(x=130, y=190)

        self.btn_login.place(x=100, y=230)
        self.btn_sign_up.place(x=200, y=230)
    
    def _on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.mainapp.destroy()
        

    def _login_web(self):
        connector: backend_connenct = self.mainapp.connector
        email, pwd = self.email_var.get(), self.password_var.get()
        login_res, l_msg = connector.login_server(email=email, password=pwd)
        if login_res:
            messagebox.showinfo(title='welcome', message=f"歡迎回來! {connector.user_name}")
            self._login()
        else:
            messagebox.showerror(title="Fail", message=f"Login fail! {l_msg}")
            self._login_offline()
    
    def _login_offline(self):
        if messagebox.askokcancel(title="offline", message=f'使用離線模式?'):
            messagebox.showwarning(title='offline', message='使用離線模式')
            self.mainapp.connector.login_status=False
            self._login()
    
    def _login(self):
        # self.mainapp.deiconify()
        self.mainapp.login()
        self.destroy()


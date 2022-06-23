import tkinter as tk
from tkinter import messagebox
import requests
from requests import session
import unicodedata
import json
from .config import SERIAL_RT_COUNT, SA_EMAIL, SA_PWD, SERVER_URL
from GUI.pop_out import PopOutInfo
import asyncio

s = requests.session()
server = SERVER_URL

class backend_connenct(object):
    def __init__(self, mainapp: tk.Tk):
        self.session = session()
        self.mainapp = mainapp
        self.login_status = False
        self.user_name = ""
        self.user_role = ""

    def show_popout(func):
        def wrap(self, *args, **kwargs):
            self.pop_out = PopOutInfo(mainapp=self.mainapp)
            self.pop_out.pop()
            # self.pop_out.update_info('連線中.')
            print('連線中')
            result = func(self, *args, **kwargs)
            self.pop_out.destroy()
            return result
        return wrap

    @show_popout
    def login_server(self, email: str = SA_EMAIL, password: str = SA_PWD, api_server = server, rt_cnt:int = 0) -> bool:
        if rt_cnt > SERIAL_RT_COUNT:
            message=f'嘗試重新連線超過{SERIAL_RT_COUNT}次'
            return (False, message)
        try:
            r = self.session.post(f"{api_server}/auth/login",
                                  json={'email':email, 'password': password})
            data = r.json()
        except Exception as e:
            e_msg = f"登入發生錯誤! 錯誤原因:{e}"
            print(e_msg)
            return (False, e_msg)
        if r.status_code == 200:
            self.user_name = data['username']
            self.user_role = data['userrole']
            self.login_status = True
            return (True, "")
        elif data['message'] == '連線不穩定，請重新在試一次!':
            print(f"連線不穩定，重試({rt_cnt})")
            rt_cnt += 1
            return self.login_server(email, password, api_server, rt_cnt)
        else:
            return (False, data['message'])

    def record_data(self, data: str):
        pass

    @show_popout
    def get_seat_list(self, rt_cnt: int=0):
        if self.login_status is False:
            print('離線模式')
            return [{'seat_name': "offline", 'id': 144, 'seat_type': 1}]
        if rt_cnt > SERIAL_RT_COUNT:
            messagebox.showwarning(title='connection failed', message=f'取得坐墊列表失敗，嘗試重新連線超過{SERIAL_RT_COUNT}次，切換至離線模式')
            self.login_status = False
            return self.get_seat_list()

        r = self.session.get(f"{server}/seat/manage")
        if r.status_code == 200:
            try:
                return r.json()['data']
            except KeyError as e:
                print(f"{e}", r.json())
                return f"{e}, {r.json()}"
        elif r.status_code == 500:
            rt_cnt += 1
            print(f'取得坐墊失敗，錯誤訊息{r.json()}，重試({rt_cnt})')
            return self.get_seat_list(rt_cnt)
        else:
            raise Exception(f"{r.json()}")

if __name__ == "__main__":
    connector = backend_connenct()
    result = connector.login_server(api_server=server)
    print(f"登入結果:{result}")
    result2 = connector.get_seat_list()
    print(f"坐墊列表:{result2}")
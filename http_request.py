from itertools import tee
import requests
from requests import session
import unicodedata
import json

s = requests.session()
server = "http://127.0.0.1:5000"
heroku_server = "https://vast-citadel-64102.herokuapp.com"
class backend_connenct(object):
    def __init__(self):
        self.session = session()
        self.login_status = False
        self.user_name = ""
        self.user_role = ""

    def login_server(self, email: str = "sa_email@example.com", password: str = "super_admin_pwd", api_server = server) -> bool:
        try:
            r = self.session.post(f"{api_server}/auth/login",
                                  json={'email':email, 'password': password})
            msg = unicodedata.normalize("NFKD", r.text)
            print(f"status={r.status_code}, text={msg}")
        except Exception as e:
            print(f"登入發生錯誤! 錯誤原因{e}" )
            return False
        if r.status_code == 200:
            data = json.loads(msg)
            self.user_name = data['username']
            self.user_role = data['userrole']
            self.login_status = True
        return True if r.status_code == 200 else False

    def record_data(self, data: str):
        pass
    # import backend
    def get_seat_list(self):
        r = self.session.get(f"{server}/seat/manage")
        return r.json()['data']

if __name__ == "__main__":
    connector = backend_connenct()
    result = connector.login_server(api_server=server)
    print(f"登入結果:{result}")
    result2 = connector.get_seat_list()
    print(f"坐墊列表:{result2}")
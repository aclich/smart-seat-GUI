import requests
from requests import session
import unicodedata
import json
from config import Config

conf = Config()

s = requests.session()
server = conf.server_url
class backend_connenct(object):
    def __init__(self):
        self.session = session()
        self.login_status = False
        self.user_name = ""
        self.user_role = ""

    def login_server(self, email: str = conf.sa_email, password: str = conf.sa_pwd, api_server = server) -> bool:
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
        if r.status_code != 200:
            raise Exception(f"{r.json()}")
        try:
            return r.json()['data']
        except KeyError as e:
            print(f"{e}", r.json())
            return f"{e}, {r.json()}"

if __name__ == "__main__":
    connector = backend_connenct()
    result = connector.login_server(api_server=server)
    print(f"登入結果:{result}")
    result2 = connector.get_seat_list()
    print(f"坐墊列表:{result2}")
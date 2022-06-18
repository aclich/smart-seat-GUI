
SERVER_URL = "http://localhost:5000"
SA_EMAIL = "email@example.com"
SA_PWD = "password"
DEFAULT_BOARD_MODE = 3
SERIAL_RT_COUNT = 20
CLASS_MAP = {
  1:"坐姿-正",
  2:"坐姿-偏左",
  3:"坐姿-偏右",
  4:"坐姿-翹右腳",
  5:"坐姿-翹左腳",
  6:"坐姿-翹右二郎腿",
  7:"坐姿-翹左二郎腿",
  8:"後仰"
}

DATA_ORDER = [0,1,2,3,16,4,5,6,7,17,8,9,10,11,18,12,13,14,15,19,20,21,22,23,24]

class Config(object):
    def __init__(self) -> None:
        self.server_url = SERVER_URL
        self.sa_email = SA_EMAIL
        self.sa_pwd = SA_PWD
        self.default_board_mode = DEFAULT_BOARD_MODE
        self.class_map = CLASS_MAP
        self.serial_rt_count = SERIAL_RT_COUNT

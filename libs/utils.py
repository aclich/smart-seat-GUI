from datetime import datetime, timedelta
import json
import os
import threading

int2hex: str = lambda i=0: hex(i)[2:]

def pressure_cvt_color(pres: int) -> str:
    '''
    將壓力轉換成HEX色碼字串
    <=512 green -> yellow
    >= 512 yellow -> red
    '''
    scale = 0.499
    if (pres <= 512):                                #如果壓力小於一半，顏色由綠變黃
        if pres < 0:
            return "#00FF00"
        clr = f"#{int2hex(int(pres *scale)).zfill(2)}FF00"
    else:                                                    #如果壓力大於一半，顏色由黃變紅
        if pres > 1026:
            return "#FF0000"
        diff = 255 - int((pres - 512)*scale)
        clr = f"#FF{int2hex(diff).zfill(2)}00"
    return clr.upper()

def sit_pose_static(pose_dict: dict) -> dict:
    static_dict = {}
    total = pose_dict['總計']
    for k, v in pose_dict.items():
        if k != '總計':
            static_dict[k] = f"{(round(v / total * 100, 2))}%"
    return static_dict

def carry_time(seconds: int) -> str:
    s_sec = str(seconds % 60)
    s_min = str(seconds // 60)

    return f"Timer: {s_min.zfill(2)} : {s_sec.zfill(2)} s"

class BufferData(threading.Thread):
    def __init__(self, data_dict:dict, file_path:str):
        threading.Thread.__init__(self)
        self.data_dict = data_dict
        self.file_path = file_path

    def run(self):
        print('\nbuffer thread-run')
        js = []
        if os.path.exists(self.file_path):
            js = json.load(open(self.file_path, "r", encoding='utf-8'))
        if js:
            last = datetime.strptime(js[-1]['time'], "%Y%m%d %H:%M:%S")
            now = datetime.strptime(self.data_dict['time'], "%Y%m%d %H:%M:%S")
            if now - last < timedelta(seconds=20):
                return
        js.append(self.data_dict)
        json.dump(js, open(self.file_path, 'w+', encoding='utf-8'), ensure_ascii=False, indent=4)
        print('buffer thread done')

def check_data_folder(base_path: str):
    data_path = os.path.join(base_path, 'data')
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
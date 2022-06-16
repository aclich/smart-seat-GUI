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

def sit_pose_static(pose_dict: dict):
    static_dict = {}
    total = pose_dict['總計']
    for k, v in pose_dict.items():
        if k != '總計':
            static_dict[k] = f"{(round(v / total * 100, 2))}%"
    return static_dict

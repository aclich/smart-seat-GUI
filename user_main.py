import json
import os
import pickle
import tkinter as tk
from datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.constants import ANCHOR, TOP, S, X
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageGrab, ImageTk

from libs.config import SA_EMAIL, SA_PWD, CLASS_MAP
from libs.http_request import backend_connenct
from libs.sensor.serial_port import init_boards
from libs.sitpos_predict.classifier import classifier
from libs.utils import pressure_cvt_color, sit_pose_static, carry_time, BufferData


sensor_seat = init_boards()

win = tk.Tk()
win.title('Welcome')
win.geometry('450x300+300+100')
win.iconbitmap("GUI/img/cushions.ico")
win.resizable(0, 0)

connector = backend_connenct(win)
predictor = classifier()

#welcome image
can = tk.Canvas(win, height=200, width=500)
image_file = tk.PhotoImage(file='GUI/img/welcome.gif')
image = can.create_image(0, 0, image=image_file, anchor='nw')
can.pack(side=TOP)

lb1 = tk.Label(win, text="User name : ")
lb1.place(x=50, y=150)

lb2 = tk.Label(win, text="Password : ")
lb2.place(x=50, y=190)

var_usr_name = tk.StringVar(value=SA_EMAIL)
entry_usr_name = tk.Entry(win, textvariable=var_usr_name)
# entry_usr_name = tk.Entry(win)
entry_usr_name.place(x=130, y=150)
var_usr_pwd = tk.StringVar(value=SA_PWD)
entry_usr_pwd = tk.Entry(win, textvariable=var_usr_pwd, show='*')
# entry_usr_pwd = tk.Entry(win, show='*')
entry_usr_pwd.place(x=130, y=190)
# data_dict = {"data": []}
data_list = []
data_order = [0,1,2,3,16,4,5,6,7,17,8,9,10,11,18,12,13,14,15,19,20,21,22,23,24]

slider_time = 0
seat_map = {}

def user_login_web():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    login_res, l_msg = connector.login_server(email=usr_name, password=usr_pwd)
    if login_res:
        print("登入成功!")
        tk.messagebox.showinfo(title='Welcome', message='Welcome! ' + connector.user_name)
        login_gui()
    else:
        print("登入失敗!")
        messagebox.showerror(title='Fail', message=f'Login fail! {l_msg}')
        if messagebox.askquestion(title='warning', message='使用離線模式?') == 'yes':
            messagebox.showinfo(title='offline', message='使用離線模式')
            connector.login_status = False
            login_gui()

#當登入成功時顯示的坐墊畫面
running = False
seconds = 0
pause_time = seconds
capture_times = 0
folder_name = ""
file_name = ""
DataInfo = {'seat_id': 144, 'gender': 1, 'weight': 0, 'height': 0}
pose_dict = {v:0 for v in [*CLASS_MAP.values(), "總計"]}

def login_gui():
    gui = tk.Toplevel(win)
    gui.geometry('1200x700+150+0')
    gui.title('User window')
    gui.iconbitmap("GUI/img/cushions.ico")
    gui.protocol("WM_DELETE_WINDOW", win.destroy)
    win.withdraw()

    mycanvas = tk.Canvas(gui, width=500, height=500, bg='black')
    mycanvas.place(x=20, y=120)
    sensors, labels, label_y = [], [], 0

    ########顯示標籤############################################
    # labframe = LabelFrame(gui, text="Sensor value", font="Arial 12", labelanchor=N)
    # labframe.place(x=550, y=15, height=780, width=130)

    for y in range(0, 500, 100):
        for x in range(0, 500, 100):
            sensors.append(mycanvas.create_rectangle(x, y, x+100, y+100, fill="white"))
            labels.append(mycanvas.create_text(x+15, y+10, text='0', state='hidden', font="微軟正黑體 12", tag="value"))

    value_vars = [tk.IntVar(value=0) for _ in range(25)]
    def show_value():
        state = 'normal' if  status.get() == 1 else 'hidden'
        for label in labels:
            mycanvas.itemconfig(label, state=state)
    

    status = IntVar()
    Checkbutton1 = Checkbutton(gui, text="顯示壓力值", font="微軟正黑體 12", variable=status, command=show_value)
    Checkbutton1.place(x=22, y=640)

    timming = tk.Label(gui, text="Timer : 00 m 00 s", font="Arial 18", width=15)
    timming.place(x=325, y=630)

    def get_data_info():
        global DataInfo
        data_info = [DataInfo['seat_name'], DataInfo['file_path'], DataInfo['height'], DataInfo['weight'], DataInfo['gender']]
        return data_info


    def update_pose_static(pose_static):
        for k, v in pose_static.items():
            pose_lbs[k].configure(text=f"{k} : {v}")

    #Start, Stop 連續顯示顏色並暫停
    def btn_color_continuously():
        global pose_dict
        if running :
            print("btn_continue", end='')
            data_dict = {}
            seat_name, file_path, height, weight, gender = get_data_info()
            seat = get_seat(seat_name)
            print("  get-data", end='')
            data = sensor_seat.get_sensor_value()
            print('-done', end='')

            x = [*data, int(gender), float(height), float(weight)]
            print('  predict', end='')
            sit_pose: str = predictor.predict(model="RF", x=x, cvt_ch=False)
            print('-done', end='')

            data_dict['data'] = data
            data_dict['seat_id'] = seat['id']
            data_dict['seat_type'] = seat['seat_type']
            data_dict['time'] = datetime.strftime(datetime.now(), "%Y%m%d %H:%M:%S")
            data_dict['gender'] = gender
            data_dict['height'] = height
            data_dict['weight'] = weight
            data_dict['sit_pos'] = str(sit_pose)

            sit_pose_str_var.set(f'3. 當前坐姿 : {CLASS_MAP[sit_pose]}')
            pose_dict[CLASS_MAP[sit_pose]] += 1
            pose_dict['總計'] += 1
            update_pose_static(sit_pose_static(pose_dict))
            if seconds % 30 == 1:
                print('  bufferdata', end='')
                BufferData(data_dict, file_path).start()
                print('-done', end='')
            # data_list.append(data_dict)

            print('  config-gui', end='')
            if data_dict['data'] == []:                                                 #跳過delay時間
                pass    
            else:
                for sensor, label, val in zip(sensors, labels, data_dict['data']):
                    mycanvas.itemconfig(sensor, fill=pressure_cvt_color(val))           # 塗顏色
                    mycanvas.itemconfig(label, text=f"{val}")                                              # 寫壓力值
            print('-done')
        gui.after(100, btn_color_continuously)
    
    def set_timming():
        global seconds
        timming.configure(text=carry_time(seconds))
  
    def start():
        """Enable running by setting the global flag to True."""
        print('start')
        global running
        global seconds
        global pause_time
        running = True
        if seconds < 9999:
            print('start-run')
            seconds += 1 
            set_timming()
            gui.after(1000, start)                           #每過500ms刷新一次
        else:
            print('stop')
            seconds = pause_time
            running = False


    def stop():
        """Stop running by setting the global flag to False."""
        global running
        global seconds
        global pause_time
        running = False
        pause_time = seconds
        seconds = 9999
        
    def get_json():
        folder_name, file_path, height, weight, gender = get_data_info()
        json_file = open(file_path, "w+", encoding="utf-8")
        json.dump(data_list, json_file, indent=1, ensure_ascii=False)
        print(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")+"\n")
        print(data_list)

    def reset():
        global seconds
        global data_list
        global pause_time
        global pose_dict
        seconds, pause_time = 0, 0
        pose_dict = {v:0 for v in [*CLASS_MAP.values(), "總計"]}
        update_pose_static({v:'' for v in [*CLASS_MAP.values()]})
        set_timming()
        for sensor, label in zip(sensors, labels):
            mycanvas.itemconfig(sensor, fill="white")
            mycanvas.itemconfig(label, text='0')
        data_list = []


    def data_info(): #Open
        global DataInfo
        data = tk.Toplevel(gui)
        data.geometry('320x200+200+200')
        data.title('File name')
        Label = tk.Label(data, text="選擇坐墊 : ", font="微軟正黑體 12")
        Label.place(x=20, y=20)
        select_seat = ttk.Combobox(data, value=get_user_seat_list(), width=15, state="readonly", font="微軟正黑體 12")
        select_seat.current(0)
        select_seat.place(x=110, y=20)
        gender_l = tk.Label(data, text="性別 (Gender) :", font="微軟正黑體 12")
        gender_l.place(x=20, y=60)
        gen_cb = ttk.Combobox(data, value=["男", "女"], width=6, state="readonly", font="微軟正黑體 12")
        gen_cb.place(x=140, y=60)
        Hei = tk.Label(data, text="身高 (Height) : ", font="微軟正黑體 12")
        Hei.place(x=20, y=100)
        Entry2 = tk.Entry(data, width=10)
        Entry2.place(x=140, y=100)
        cm = tk.Label(data, text="cm", font="微軟正黑體 12")
        cm.place(x=200, y=100)
        Wei = tk.Label(data, text="體重 (Weight) : ", font="微軟正黑體 12")
        Wei.place(x=20, y=140)
        Entry3 = tk.Entry(data, width=10)
        Entry3.place(x=140, y=140)
        kg = tk.Label(data, text="kg", font="微軟正黑體 12")
        kg.place(x=200, y=140)

        def check_file_name():
            global DataInfo

            seat_name = select_seat.get()
            file_name = seat_name + f"_{datetime.now().strftime('%y%m%d_%H%M')}.json"
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", file_name)
            if os.path.exists(file_path):
                messagebox.showwarning("相同記錄檔名已存在!")
                return
            gender, height, weight = {"男": 1, "女": 2}[gen_cb.get()], Entry2.get(), Entry3.get()
            info = f"坐墊名稱:{seat_name}  性別:{gen_cb.get()}  身高:{height}cm  體重:{weight}kg"
            print(info)
            info_label['text'] = info
            DataInfo = {'file_path': file_path, 'seat_name': seat_name, 'gender': gender, 'height': height, 'weight': weight}
            messagebox.showinfo("showinfo", "Succesful!")
            data.destroy()
            gui.update()

        Button = tk.Button(data, text="確定", command=check_file_name, font="微軟正黑體 10")
        Button.place(x=250, y=135)

                                                                                                                                                                            
    def get_user_seat_list() -> list:                              #取得坐墊型號
        seat_list = connector.get_seat_list()
        cb_value = []
        for d in seat_list:
            seat_map[d['seat_name']] = {"id": d['id'], "seat_type": d['seat_type']}
            cb_value.append(d['seat_name'])
        return cb_value
    
    def get_seat(seat_name: str) -> dict:
        return seat_map[seat_name]

    def running_mode():
        global slider_time
        slider_time = 0
        try:
            _ = get_data_info()
        except Exception as e:
            messagebox.showwarning(title='warning', message="請先輸入使用者資料!")
            return

        if running:
            messagebox.showwarning('請先暫停!')
        elif second_cb.get() == "連續模式":
            start()
        else:
            setting = tk.Toplevel(gui)
            setting.geometry('360x150+200+200')
            setting.title('Time')
            label = tk.Label(setting, text="設定時間 : ", font="微軟正黑體 12")
            label.place(x=20, y=45)
            slider = tk.Scale(setting, from_=5, to=60, length=200, resolution=5, orient=HORIZONTAL)
            slider.place(x=100, y=30)
            label2 = tk.Label(setting, text="min", font="微軟正黑體 12")
            label2.place(x=305, y=45)


            def set_ok():
                global running
                global seconds
                global slider_time
                global pause_time
                running = True
                slider_time = slider.get()
                setting.destroy()
                seconds = pause_time
                gui.after(1, time_ok)

            def time_ok():
                global running
                global seconds
                global slider_time
                if running:
                    if seconds < int(slider_time)*60:
                        seconds += 1 
                        set_timming()
                        gui.after(1000, time_ok)                       #每過1000ms刷新一次
                    else: 
                        # get_json()
                        seconds = 9999
                        running = False
                
            Button = tk.Button(setting, text="確定", font="微軟正黑體 10", command=set_ok)
            Button.place(x=160, y=90)

    global logo, logo2, logo3
    logo_pic = Image.open('GUI/img/Smart-Seat_logo.png').resize((500, 80))
    logo = ImageTk.PhotoImage(logo_pic)
    logo_lb1 = tk.Label(gui, image=logo)
    logo_lb1.place(x=20, y=20)

    logo_pic2 = Image.open('GUI/img/Introduction.png').resize((400, 100))
    logo2 = ImageTk.PhotoImage(logo_pic2)
    logo_lb2 = tk.Label(gui, image=logo2)
    logo_lb2.place(x=650, y=20)

    first_step = LabelFrame(gui, text="", labelanchor=N)
    first_step.place(x=550, y=130, width=620, height=40)

    first_lb = tk.Label(first_step, text="1. 輸入使用者資料 : ", font="微軟正黑體 12")
    first_lb.place(x=3, y=3)

    first_btn = tk.Button(first_step, text="Open", command=data_info)
    first_btn.place(x=150, y=3)

    info_label = tk.Label(first_step, text='', font="微軟正黑體 10", width=45)
    info_label.place(x=200, y=6)

    second_step = LabelFrame(gui, text="")
    second_step.place(x=550, y=180, width=620, height=40)

    second_lb = tk.Label(second_step, text="2. 選擇紀錄模式 : ", font="微軟正黑體 12")
    second_lb.place(x=3, y=3)

    second_cb = ttk.Combobox(second_step, value=["連續模式", "固定模式"], width=8, state="readonly", font="微軟正黑體 12")
    second_cb.current(0)
    second_cb.place(x=140, y=3)

    second_btn_start = tk.Button(second_step, text="Start", command=running_mode)
    second_btn_start.place(x=245, y=3)

    second_btn_stop = tk.Button(second_step, text="Stop", command=stop)
    second_btn_stop.place(x=290, y=3)

    third_step = LabelFrame(gui, text="")
    third_step.place(x=550, y=230, width=620, height=40)

    sit_pose_str_var = tk.StringVar(value='3. 當前坐姿 : ')
    third_lb = tk.Label(third_step, textvariable=sit_pose_str_var, font="微軟正黑體 12")
    third_lb.place(x=3, y=3)

    fourth_step = LabelFrame(gui, text="")
    fourth_step.place(x=550, y=280, width=620, height=40)

    fourth_lb = tk.Label(fourth_step, text="4. 上傳資料 : ", font="微軟正黑體 12")
    fourth_lb.place(x=3, y=3)

    def choose():
        choose_file = askopenfilename(title='select json record',
                                      initialdir='./',
                                      filetypes=[['json record', '*.json']])
        if choose_file =="":
            upload_file_var.set('')
        else:
            upload_file_var.set(choose_file)

    upload_file_var = tk.StringVar(value='')
    fourth_lb_path = tk.Label(fourth_step, textvariable=upload_file_var)
    fourth_lb_path.place(x=175, y=3)

    fourth_btn_choose = tk.Button(fourth_step, text="選擇", font="微軟正黑體 8", command=choose)
    fourth_btn_choose.place(x=105, y=3)

    fourth_btn_upload = tk.Button(fourth_step, text="上傳", font="微軟正黑體 8", command=lambda: connector.record_data(upload_file_var.get()))
    fourth_btn_upload.place(x=140, y=3)


    fifth_step = LabelFrame(gui, text="", bg="Beige")
    fifth_step.place(x=550, y=330, width=620, height=300)

    logo_pic3 = Image.open('GUI/img/seat.png').resize((200, 60))
    logo3 = ImageTk.PhotoImage(logo_pic3)
    logo_lb3 = tk.Label(fifth_step, image=logo3)
    logo_lb3.place(x=200, y=0)

    pose_lbs = {}
    for i in range(1,len(CLASS_MAP)+1):
        x = 20 if i < 5 else 300
        y = 80 + 50*((i-1)%4)
        p_lb = tk.Label(fifth_step, text=f"{CLASS_MAP[i]} : ", font="微軟正黑體 12", bg="Beige")
        p_lb.place(x=x, y=y)
        pose_lbs[CLASS_MAP[i]] = p_lb

    clean_btn = tk.Button(gui, text="清除", font="微軟正黑體 10", command=reset)
    clean_btn.place(x=850, y=630)

    version = tk.Label(gui, text="Version 1.0", font="Arial 10")
    version.place(x=1120, y=680)

    gui.after(0, btn_color_continuously)



#註冊畫面、檢查帳號是否存在
def usr_sign_up():
    def sign_to_interface():
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        if np != npf:
            tk.messagebox.showerror('Error', 'Password and confirm password must be the same!')
        elif nn in exist_usr_info:
            tk.messagebox.showerror('Error', 'The user has already signed up!')
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tk.messagebox.showinfo('Successfully', 'Your account can be used now!')
            win_sign_up.destroy()
    win_sign_up = tk.Toplevel(win)
    win_sign_up.geometry('350x200')
    win_sign_up.title('Sign up window')

    new_name = tk.StringVar()
    new_name.set('example@python.com')
    tk.Label(win_sign_up, text='User name: ').place(x=10, y= 10)
    entry_new_name = tk.Entry(win_sign_up, textvariable=new_name)
    entry_new_name.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(win_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(win_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(win_sign_up, text='Confirm password: ').place(x=10, y= 90)
    entry_usr_pwd_confirm = tk.Entry(win_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)

    btn_comfirm_sign_up = tk.Button(win_sign_up, text='Sign up', command=sign_to_interface)
    btn_comfirm_sign_up.place(x=150, y=130)


# login and sign up button
btn_login = tk.Button(win, text='Login', command=user_login_web)
btn_login.place(x=100, y=230)
btn_sign_up = tk.Button(win, text='Sign up', command=usr_sign_up)
btn_sign_up.place(x=200, y=230)

win.mainloop()

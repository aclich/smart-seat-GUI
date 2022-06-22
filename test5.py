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

from libs.config import Config
from libs.http_request import backend_connenct
from libs.sensor.serial_port import init_boards
from libs.sitpos_predict.classifier import classifier
from libs.utils import pressure_cvt_color, sit_pose_static, carry_time

conf = Config()
connector = backend_connenct()
predictor = classifier()

sensor_seat = init_boards()

win = tk.Tk()
win.title('Welcome')
win.geometry('450x300+300+100')
win.iconbitmap("img/cushions.ico")
win.resizable(0, 0)

#welcome image
can = tk.Canvas(win, height=200, width=500)
image_file = tk.PhotoImage(file='GUI/img/welcome.gif')
image = can.create_image(0, 0, image=image_file, anchor='nw')
can.pack(side=TOP)

lb1 = tk.Label(win, text="User name : ")
lb1.place(x=50, y=150)

lb2 = tk.Label(win, text="Password : ")
lb2.place(x=50, y=190)

var_usr_name = tk.StringVar()
var_usr_name.set("admin")
entry_usr_name = tk.Entry(win, textvariable=var_usr_name)
# entry_usr_name = tk.Entry(win)
entry_usr_name.place(x=130, y=150)
var_usr_pwd = tk.StringVar()
var_usr_pwd.set("admin")
entry_usr_pwd = tk.Entry(win, textvariable=var_usr_pwd, show='*')
# entry_usr_pwd = tk.Entry(win, show='*')
entry_usr_pwd.place(x=130, y=190)
# data_dict = {"data": []}
data_list = []
data_order = [0,1,2,3,16,4,5,6,7,17,8,9,10,11,18,12,13,14,15,19,20,21,22,23,24]

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
capture_times = 0
folder_name = ""
file_name = ""
DataInfo = {'seat_id': 144, 'gender': 1, 'weight': 0, 'height': 0}

def login_gui():
    gui = tk.Toplevel(win)
    gui.geometry('1200x700+150+0')
    gui.title('User window')
    gui.iconbitmap("img/cushions.ico")

    mycanvas = tk.Canvas(gui, width=500, height=500, bg='black')
    mycanvas.place(x=20, y=120)
    sensors, labels, label_y = [], [], 0

    ########顯示標籤############################################
    # labframe = LabelFrame(gui, text="Sensor value", font="Arial 12", labelanchor=N)
    # labframe.place(x=550, y=15, height=780, width=130)

    for y in range(0, 500, 100):
        for x in range(0, 500, 100):
            sensors.append(mycanvas.create_rectangle(x, y, x+100, y+100, fill="white"))
            labels.append(mycanvas.create_text(x+15, y+10, text='sss', state='hidden', font="微軟正黑體 12", tag="value"))

    value_vars = [tk.IntVar(value=0) for _ in range(25)]
    def show_value():
        state = 'normal' if  status.get() == 1 else 'hidden'
        for label in labels:
            mycanvas.itemconfig(label, state=state)
    

    status = IntVar()
    Checkbutton1 = Checkbutton(gui, text="顯示壓力值", font="微軟正黑體 12", variable=status, command=show_value)
    Checkbutton1.place(x=22, y=640)

    timming = tk.Label(gui, text="Timer : ", font="Arial 18", width=15)
    timming.place(x=395, y=630)
    timer_lb = tk.Label(gui, text="0 s", font="Arial 18", width=4)
    timer_lb.place(x=470, y=630)

    def get_data_info():
        global DataInfo
        data_info = [DataInfo['seat_name'], DataInfo['file_name'], DataInfo['height'], DataInfo['weight'], DataInfo['gender']]
        return data_info

    #Start, Stop 連續顯示顏色並暫停
    def btn_color_continuously():
        if running :
            data_dict = {}
            seat_name, file_name, height, weight, gender = get_data_info()
            # data_dict['name'] = file_name[:-4]
            x = [*data_dict['data'], int(data_dict['gender']), float(data_dict['height']), float(data_dict['weight'])]
            sit_pose: str = predictor.predict(model="RF", x=x)
            status_lb = tk.Label(gui, text=sit_pose, font="微軟正黑體 12", width=15)
            seat = get_seat(seat_name)
            data_dict['seat_id'] = seat['id']
            data_dict['seat_type'] = seat['seat_type']
            data_dict['time'] = datetime.strftime(datetime.now(), "%Y%m%d %H:%M:%S")
            data_dict['data'] = sensor_seat.get_sensor_value()
            data_dict['gender'] = gender
            data_dict['height'] = height
            data_dict['weight'] = weight
            data_dict['sit_pos'] = sit_pose

            status_lb.place(x=180, y=760)
            data_list.append(data_dict)

            if data_dict['data'] == []:                                                 #跳過delay時間
                pass    
            else:
                for sensor, label, val in zip(sensors, labels, data_dict['data']):
                    mycanvas.itemconfig(sensor, fill=pressure_cvt_color(val))           # 塗顏色
                    mycanvas.itemconfig(label, text=f"{val}")                                              # 寫壓力值
                    

            
        gui.after(100, btn_color_continuously)
    
    def set_timming():
        global seconds
        timming.configure(text=f'Timer: {carry_time(seconds)}')
  
    def start():
        """Enable running by setting the global flag to True."""
        global running
        global seconds
        running = True
        if seconds < 9999 :
            seconds += 1 
            gui.after(1000, start)                           #每過500ms刷新一次
            set_timming()
        else : 
            running = False


    def stop():
        """Stop running by setting the global flag to False."""
        global running
        global seconds
        running = False
        seconds = 9999
        
    def get_json():
        folder_name, file_name, height, weight, gender = get_data_info()
        data_json = {}
        data_json['name'] = file_name[:-4]
        data_json['data'] = data_list
        json_file = open(os.path.join('./data', f"{data_json['name']}.json"), "w+", encoding="utf-8")
        json.dump(data_list, json_file, indent=1, ensure_ascii=False)
        print(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")+"\n")
        print(data_json)

    def reset():
        global seconds
        global data_list
        seconds = 0
        timer_lb.config(text="%i s" % seconds)
        for sensor in sensors:
            mycanvas.itemconfig(sensor, fill="white")
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
            file_name = seat_name + f"_{datetime.now().strftime('%h%m%d %H:%M')}.txt"
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", file_name)
            if os.path.exists(data_path):
                messagebox.showwarning("相同記錄檔名已存在!")
                return
            gender, height, weight = {"男": 1, "女": 2}[gen_cb.get()], Entry2.get(), Entry3.get()
            info_label['text'] = f"坐墊名稱:{seat_name} 性別:{gen_cb.get()} 身高:{height}cm 體重:{weight}kg"
            DataInfo = {'file_name': file_name, 'seat_name': seat_name, 'gender': gender, 'height': height, 'weight': weight}
            messagebox.showinfo("showinfo", "Succesful!")
            data.destroy()

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



    # Label2 = tk.Label(gui, text="File : ", font="Arial 12")
    # Label2.place(x=120, y=580)

    # Label3 = tk.Label(gui, text="Status : ", font="Arial 12")
    # Label3.place(x=120, y=640)

    # Label4 = tk.Label(gui, text="Select : ", font="Arial 12")
    # Label4.place(x=120, y=700)

    # Label5 = tk.Label(gui, text="Status : ", font="Arial 12")
    # Label5.place(x=120, y=760)
    

    # (1)坐姿-正 (2)坐姿-偏左 (3)坐姿-偏右 (4)坐姿-翹右腳 (5)坐姿-翹左腳 (6)坐姿-翹右二郎腿 
    # (7)坐姿-翹左二郎腿  (8)後仰
    # cb = ttk.Combobox(gui, value=["1", "2", "3", "4", "5", 
    #                                 "6", "7", "8"], width=16, state="readonly")
    # cb.current(0)
    # cb.place(x=180, y=640)

    
    # cb2 = ttk.Combobox(gui, value=get_user_seat_list(), width=16, state="readonly")             #顯示使用者帳號中已註冊的坐墊
    # cb2.current(0)
    # cb2.place(x=180, y=700)


    # sit_frame = LabelFrame(gui, text="坐姿對照表", labelanchor=N, font="標楷體 11 ",fg="brown")
    # sit_frame.place(x=330, y=630, width=200, height=90)
    # Label = tk.Label(sit_frame, text="(1)坐姿-正 (2)坐姿-偏左\n(3)坐姿-偏右 (4)坐姿-翹右腳\n(5)坐姿-翹左腳(6)坐姿-翹右二郎腿\n(7)坐姿-翹左二郎腿 (8)後仰", font="微軟正黑體 9")
    # Label.place(x=0, y=0)


    # file = tk.Button(gui, text="Open", command=data_info)
    # file.place(x=120, y=530)

    # bt_60s = tk.Button(gui, text="60sec", command=start_60s)
    # bt_60s.place(x=180, y=530) 

    # bt_0s = tk.Button(gui, text="Reset", command=reset)
    # bt_0s.place(x=240, y=530)

    # upload_data = tk.Button(gui, text="Upload")
    # upload_data.place(x=300, y=530)

    def running_mode():
        
        if second_cb.get() == "連續模式":
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

            def time_ok():
                global running
                global seconds
                running = True

                if seconds < int(slider.get())*60 :
                    seconds += 1 
                    gui.after(1000, time_ok)                           #每過1000ms刷新一次

                else : 
                    get_json()
                    running = False
                set_timming()
                
            Button = tk.Button(setting, text="確定", font="微軟正黑體 10", command=time_ok)
            Button.place(x=160, y=90)

    global logo, logo2, logo3
    logo_pic = Image.open('img/Smart-Seat_logo.png').resize((500, 80))
    logo = ImageTk.PhotoImage(logo_pic)
    logo_lb1 = tk.Label(gui, image=logo)
    logo_lb1.place(x=20, y=20)

    logo_pic2 = Image.open('img/Introduction.png').resize((400, 100))
    logo2 = ImageTk.PhotoImage(logo_pic2)
    logo_lb2 = tk.Label(gui, image=logo2)
    logo_lb2.place(x=650, y=20)

    first_step = LabelFrame(gui, text="", labelanchor=N)
    first_step.place(x=550, y=130, width=620, height=40)

    first_lb = tk.Label(first_step, text="1. 輸入使用者資料 : ", font="微軟正黑體 12")
    first_lb.place(x=3, y=3)

    first_btn = tk.Button(first_step, text="Open", command=data_info)
    first_btn.place(x=150, y=3)

    info_label = tk.Label(first_step, text='', font="微軟正黑體 12", width=320)
    info_label.place(x=180, y=3)

    second_step = LabelFrame(gui, text="")
    second_step.place(x=550, y=180, width=620, height=40)

    second_lb = tk.Label(second_step, text="2. 選擇紀錄模式 : ", font="微軟正黑體 12")
    second_lb.place(x=3, y=3)

    second_cb = ttk.Combobox(second_step, value=["連續模式", "固定模式"], width=8, state="readonly", font="微軟正黑體 12")
    second_cb.current(0)
    second_cb.place(x=140, y=3)

    second_btn_start = tk.Button(second_step, text="Start", command=running_mode)
    second_btn_start.place(x=245, y=3)

    second_btn_stop = tk.Button(second_step, text="Stop")
    second_btn_stop.place(x=290, y=3)

    third_step = LabelFrame(gui, text="")
    third_step.place(x=550, y=230, width=620, height=40)

    third_lb = tk.Label(third_step, text="3. 當前坐姿 : ", font="微軟正黑體 12")
    third_lb.place(x=3, y=3)

    fourth_step = LabelFrame(gui, text="")
    fourth_step.place(x=550, y=280, width=620, height=40)

    fourth_lb = tk.Label(fourth_step, text="4. 上傳資料 : ", font="微軟正黑體 12")
    fourth_lb.place(x=3, y=3)

    def choose():
        choose_file = askopenfilename()
        if choose_file =="":
            return
        else:
            fourth_lb_path.config(text=choose_file)
            print(choose_file)

    fourth_btn_choose = tk.Button(fourth_step, text="選擇", font="微軟正黑體 8", command=choose)
    fourth_btn_choose.place(x=105, y=3)

    fourth_btn_upload = tk.Button(fourth_step, text="上傳", font="微軟正黑體 8")
    fourth_btn_upload.place(x=140, y=3)

    fourth_lb_path = tk.Label(fourth_step, text="")
    fourth_lb_path.place(x=175, y=3)

    fifth_step = LabelFrame(gui, text="", bg="Beige")
    fifth_step.place(x=550, y=330, width=620, height=300)

    logo_pic3 = Image.open('img/seat.png').resize((200, 60))
    logo3 = ImageTk.PhotoImage(logo_pic3)
    logo_lb3 = tk.Label(fifth_step, image=logo3)
    logo_lb3.place(x=200, y=0)

    fifth_lb1 = tk.Label(fifth_step, text="坐姿-正 : ", font="微軟正黑體 12", bg="Beige")
    fifth_lb1.place(x=20, y=80)

    fifth_lb2 = tk.Label(fifth_step, text="坐姿-偏左 : ", font="微軟正黑體 12", bg="Beige")
    fifth_lb2.place(x=20, y=130)

    fifth_lb3 = tk.Label(fifth_step, text="坐姿-偏右 : ", font="微軟正黑體 12", bg="Beige")
    fifth_lb3.place(x=20, y=180)

    fifth_lb4 = tk.Label(fifth_step, text="坐姿-翹右腳 : ", font="微軟正黑體 12", bg="Beige")
    fifth_lb4.place(x=20, y=230)

    fifth_lb5 = tk.Label(fifth_step, text="坐姿-翹左腳 : ", font="微軟正黑體 12", bg="Beige")
    fifth_lb5.place(x=300, y=80)

    fifth_lb6 = tk.Label(fifth_step, text="坐姿-翹右二郎腿 : ", font="微軟正黑體 12", bg="Beige")
    fifth_lb6.place(x=300, y=130)

    fifth_lb7 = tk.Label(fifth_step, text="坐姿-翹左二郎腿 : ", font="微軟正黑體 12", bg="Beige")
    fifth_lb7.place(x=300, y=180)

    fifth_lb8 = tk.Label(fifth_step, text="坐姿-後仰 : ", font="微軟正黑體 12", bg="Beige")
    fifth_lb8.place(x=300, y=230)

    clean_btn = tk.Button(gui, text="清除", font="微軟正黑體 10")
    clean_btn.place(x=850, y=630)

    version = tk.Label(gui, text="Version 1.0", font="Arial 10")
    version.place(x=1120, y=680)

    gui.after(500, btn_color_continuously)



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

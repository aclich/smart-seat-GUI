import json
import os
import pickle
import tkinter as tk
from datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.constants import ANCHOR, TOP, S, X

from PIL import ImageGrab

from libs.config import CLASS_MAP, Config
from libs.http_request import backend_connenct
from libs.sensor.serial_port import init_boards
from libs.sitpos_predict.classifier import classifier
from libs.utils import pressure_cvt_color, sit_pose_static

predictor = classifier()

conf = Config()
connector = backend_connenct()
# try:
sensor_seat = init_boards()
# except:
#     print("沒有偵測到坐墊!")

win = tk.Tk()
win.title('Welcome')
win.geometry('450x300+300+100')
win.resizable(0, 0)

#welcome image
can = tk.Canvas(win, height=200, width=500)
image_file = tk.PhotoImage(file='welcome.gif')
image = can.create_image(0, 0, image=image_file, anchor='nw')
can.pack(side=TOP)

lb1 = tk.Label(win, text="User name : ")
lb1.place(x=50, y=150)

lb2 = tk.Label(win, text="Password : ")
lb2.place(x=50, y=190)

var_usr_name = tk.StringVar()
var_usr_name.set(conf.sa_email)
entry_usr_name = tk.Entry(win, textvariable=var_usr_name)
# entry_usr_name = tk.Entry(win)
entry_usr_name.place(x=130, y=150)
var_usr_pwd = tk.StringVar()
var_usr_pwd.set(conf.sa_pwd)
entry_usr_pwd = tk.Entry(win, textvariable=var_usr_pwd, show='*')
# entry_usr_pwd = tk.Entry(win, show='*')
entry_usr_pwd.place(x=130, y=190)
# data_dict = {"data": []}
data_list = []

seat_map = {}

pose_dict = {v:0 for v in [*CLASS_MAP.values(), "總計"]}

# 登入按鈕檢查帳號是否存在
def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try : 
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError :
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin':'admin'}
            pickle.dump(usrs_info, usr_file)
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='Welcome', message='Welcome! ' + usr_name)
            connector.login_server()  #記得要刪掉
            login_gui()
        else : 
            tk.messagebox.showerror(message='Error, your password is wrong, please try again!')
    else : 
        is_sign_up = tk.messagebox.askyesno('Oh! ', 'You have not signed up yet. Do you want to sign up now?')
        if is_sign_up:
            usr_sign_up()

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
        tk.messagebox.showinfo(title='Fail', message=f'Login fail! {l_msg}')

#當登入成功時顯示的坐墊畫面
running = False
seconds = 0
capture_times = 0
folder_name = ""
file_name = ""
value_list = list()
value_list2 = list()

def login_gui():
    
    gui = tk.Toplevel(win)
    gui.geometry('700x800+150+0')
    gui.title('User window')

    mycanvas = tk.Canvas(gui, width=500, height=500, bg='black')
    mycanvas.place(x=20, y=20)
    sensors, labels, label_y = [], [], 0

    ########顯示標籤############################################
    labframe = LabelFrame(gui, text="Sensor value", font="Arial 12", labelanchor=N)
    labframe.place(x=550, y=15, height=780, width=130)

    for y in range(0, 500, 100):
        for x in range(0,500, 100):
            sensors.append(mycanvas.create_rectangle(x, y, x+100, y+100, fill="white"))
            l_y = label_y*30+10
            tk.Label(labframe, text=f"Sensor{label_y+1} : ").place(x=5, y=l_y)
            s_label =  tk.Label(labframe, text=0)
            s_label.place(x=65, y=l_y)
            labels.append(s_label)
            label_y += 1

    timming = tk.Label(gui, text="Timer : ", font="Arial 18", width=5)
    timming.place(x=395, y=530)
    timer_lb = tk.Label(gui, text="0 s", font="Arial 18", width=4)
    timer_lb.place(x=470, y=530)

    def get_data_info():
        data_info = open("data_name.txt", "r").read().split(",")
        return data_info

    #Start, Stop 連續顯示顏色並暫停
    def btn_color_continuously():
        global pose_dict
        if running:
            data_dict = {}
            folder_name, file_name, height, weight, gender = get_data_info()
            # data_dict['name'] = file_name[:-4]
            seat = get_seat(cb2.get())
            data_dict['seat_id'] = seat['id']
            data_dict['seat_type'] = seat['seat_type']
            data_dict['time'] = datetime.strftime(datetime.now(), "%Y%m%d %H:%M:%S")
            data_dict['data'] = sensor_seat.get_sensor_value()
            data_dict['sit_pos'] = cb.get()
            data_dict['gender'] = gender
            data_dict['height'] = height
            data_dict['weight'] = weight
            x = [*data_dict['data'], int(data_dict['gender']), float(data_dict['height']), float(data_dict['weight'])]
            sit_pose: str = predictor.predict(model="RF", x=x)
            pose_dict[sit_pose] += 1
            pose_dict["總計"] += 1
            print(sit_pose_static(pose_dict))
            status_lb = tk.Label(gui, text=sit_pose, font="微軟正黑體 12", width=15)
            status_lb.place(x=180, y=760)
            data_list.append(data_dict)

            if data_dict['data'] == []:                                                 #跳過delay時間
                pass    
            else:
                for sensor, label, val in zip(sensors, labels, data_dict['data']):
                    mycanvas.itemconfig(sensor, fill=pressure_cvt_color(val))           # 塗顏色
                    label['text'] = val                                                 # 寫壓力值

            
        gui.after(100, btn_color_continuously)
  
    def start():
        """Enable running by setting the global flag to True."""
        global running
        global seconds
        running = True
        if seconds < 9999 :
            seconds += 1 
            gui.after(1000, start)                           #每過500ms刷新一次
            timer_lb.configure(text="%i s" % seconds)
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


    def start_60s():
        global running
        global seconds
        running = True
        x1 = mycanvas.winfo_rootx()/0.67
        y1 = mycanvas.winfo_rooty()/0.67
        x2 = x1 + (mycanvas.winfo_width()/0.67)
        y2 = y1 + (mycanvas.winfo_height()/0.67)

        if seconds <15 :
            seconds += 1 
            pic_name = "Photo" + str(seconds) + ".png"
            folder_name = get_data_info()[0]
            #ImageGrab.grab(bbox=(x1, y1, x2, y2)).save('/Users/a3974/Desktop/Python code/%s/%s' %(folder_name, pic_name))
            ImageGrab.grab(bbox=(x1, y1, x2, y2)).save(os.path.join(folder_name, pic_name))
            gui.after(1000, start_60s)                           #每過1000ms刷新一次

        else : 
            get_json()
            running = False
        timer_lb.configure(text="%i s" % seconds)


    def capture():
        global capture_times
        capture_times += 1
        x1 = mycanvas.winfo_rootx()/0.67
        y1 = mycanvas.winfo_rooty()/0.67
        x2 = x1 + (mycanvas.winfo_width()/0.67)
        y2 = y1 + (mycanvas.winfo_height()/0.67)
        data_name = open("data_name.txt", "r").read()
        data_name = data_name.split(",")
        folder_name = data_name[0]
        capture_name = "Status"+str(capture_times)+".png"
        #ImageGrab.grab(bbox=(x1, y1, x2, y2)).save('/Users/a3974/Desktop/Python code/%s/%s' %(folder_name, capture_name))
        ImageGrab.grab(bbox=(x1, y1, x2, y2)).save(os.path.join(folder_name, capture_name))



    def reset():
        global seconds
        global data_list
        seconds = 0
        timer_lb.config(text="%i s" % seconds)
        for sensor in sensors:
            mycanvas.itemconfig(sensor, fill="white")
        data_list = []


    def data_info(): #Open
        global file_name
        data = tk.Toplevel(gui)
        data.geometry('420x200+200+200')
        data.title('File name')
        Label = tk.Label(data, text="請輸入此筆紀錄的名稱 : ")
        Label.place(x=20, y=20)
        Entry = tk.Entry(data, width=25)
        Entry.place(x=160, y=20)
        gender = tk.Label(data, text="性別 (Gender) :")
        gender.place(x=20, y=60)
        gen_cb = ttk.Combobox(data, value=["男", "女"], width=6, state="readonly")
        gen_cb.place(x=115, y=60)
        Hei = tk.Label(data, text="身高 (Height) : ")
        Hei.place(x=20, y=100)
        Entry2 = tk.Entry(data, width=10)
        Entry2.place(x=115, y=100)
        cm = tk.Label(data, text="cm")
        cm.place(x=170, y=100)
        Wei = tk.Label(data, text="體重 (Weight) : ")
        Wei.place(x=20, y=140)
        Entry3 = tk.Entry(data, width=10)
        Entry3.place(x=115, y=140)
        kg = tk.Label(data, text="kg")
        kg.place(x=170, y=140)

        def check_file_name():
            gen_data = gen_cb.get()
            if gen_data == "男":
                gen_data = "1"
            else:
                gen_data = "2"
            cm_data = "身高 : "+ Entry2.get() + "cm"
            kg_data = "體重 : "+ Entry3.get() + "kg"
            
            folder_name = Entry.get()
            file_name = Entry.get() + "_record.txt"
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            if not os.path.isdir(data_path):
                os.mkdir(data_path)
            folder_name = os.path.join(data_path, folder_name)
            print(folder_name)
            if os.path.isdir(folder_name):

                messagebox.showerror("Error", "The file name is already exists!")
                return()
            else:
                with open("data_name.txt", "w+") as f:
                    os.mkdir(folder_name)
                    data_list = [folder_name, ",", file_name, ",", Entry2.get(), ",", Entry3.get(), ",", gen_data]
                    f.writelines(data_list)
                    messagebox.showinfo("showinfo", "Succesful!")
                    #data.destroy()
                    label_name = tk.Label(gui, text=file_name, font="Arial 12")
                    label_name.place(x=160, y=580)
                    profile_cm_kg = tk.Label(gui, text="性別 : "+gen_cb.get()+"  "+cm_data+"  "+kg_data, font="微軟正黑體 10")
                    profile_cm_kg.place(x=330, y=580)
                    data.destroy()

        Button = tk.Button(data, text="確定", command=check_file_name)
        Button.place(x=350, y=15)

                                                                                                                                                                            
    def get_user_seat_list() -> list:                              #取得坐墊型號
        seat_list = connector.get_seat_list()
        cb_value = []
        for d in seat_list:
            seat_map[d['seat_name']] = {"id": d['id'], "seat_type": d['seat_type']}
            cb_value.append(d['seat_name'])
        return cb_value
    
    def get_seat(seat_name: str) -> dict:
        return seat_map[seat_name]

    def save():
        status_name = cb.get()
        folder_name = get_data_info()[0]
        fp = open(os.path.join(folder_name, "Status.txt"), "a+")
        fp.write(status_name)
        fp.write("\n")
        fp.close()



    Label2 = tk.Label(gui, text="File : ", font="Arial 12")
    Label2.place(x=120, y=580)

    Label3 = tk.Label(gui, text="Status : ", font="Arial 12")
    Label3.place(x=120, y=640)

    Label4 = tk.Label(gui, text="Select : ", font="Arial 12")
    Label4.place(x=120, y=700)

    Label5 = tk.Label(gui, text="Status : ", font="Arial 12")
    Label5.place(x=120, y=760)
    

    # (1)坐姿-正 (2)坐姿-偏左 (3)坐姿-偏右 (4)坐姿-翹右腳 (5)坐姿-翹左腳 (6)坐姿-翹右二郎腿 
    # (7)坐姿-翹左二郎腿  (8)後仰
    cb = ttk.Combobox(gui, value=["1", "2", "3", "4", "5", 
                                    "6", "7", "8"], width=16, state="readonly")
    cb.current(0)
    cb.place(x=180, y=640)

    
    cb2 = ttk.Combobox(gui, value=get_user_seat_list(), width=16, state="readonly")             #顯示使用者帳號中已註冊的坐墊
    cb2.current(0)
    cb2.place(x=180, y=700)


    sit_frame = LabelFrame(gui, text="坐姿對照表", labelanchor=N, font="標楷體 11 ",fg="brown")
    sit_frame.place(x=330, y=630, width=200, height=90)
    Label = tk.Label(sit_frame, text="(1)坐姿-正 (2)坐姿-偏左\n(3)坐姿-偏右 (4)坐姿-翹右腳\n(5)坐姿-翹左腳(6)坐姿-翹右二郎腿\n(7)坐姿-翹左二郎腿 (8)後仰", font="微軟正黑體 9")
    Label.place(x=0, y=0)


    file = tk.Button(gui, text="Open", command=data_info)
    file.place(x=120, y=530)

    bt_60s = tk.Button(gui, text="60sec", command=start_60s)
    bt_60s.place(x=180, y=530) 

    bt_0s = tk.Button(gui, text="Reset", command=reset)
    bt_0s.place(x=240, y=530)

    upload_data = tk.Button(gui, text="Upload")
    upload_data.place(x=300, y=530)


    ########連續模式############################################
    start_frame = LabelFrame(gui, text="連續模式", labelanchor=N)
    start_frame.place(x=22, y=530, width=80, height=150)

    start1 = tk.Button(start_frame, text='Start', command=start)
    start1.place(x=18, y=5)

    stop1 = tk.Button(start_frame, text='Stop', command=stop)
    stop1.place(x=18, y=45)

    capture1 = tk.Button(start_frame, text='Capture', command=capture)
    capture1.place(x=10, y=85)
    ############################################################

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

def developer_mode():
    dev = tk.Toplevel(win)
    dev.geometry('370x100+200+200')
    dev.title('Check user')

    name_Label = tk.Label(dev, text="User name : ")
    name_Label.place(x=20, y=20)

    name_var = tk.StringVar()
    name_var.set("123")
    name_ent = tk.Entry(dev, width=25, textvariable=name_var)
    name_ent.place(x=100, y=20)

    pwd_Label = tk.Label(dev, text="Password :")
    pwd_Label.place(x=20, y=60)

    pwd_var = tk.StringVar()
    pwd_var.set("123")
    pwd_entry = tk.Entry(dev, width=25, textvariable=pwd_var, show="*")
    pwd_entry.place(x=100, y=60)


    def check123():
        dev_name = name_ent.get()
        dev_pwd = pwd_entry.get()
        if dev_name == "123" and dev_pwd =="123":
            tk.messagebox.showinfo(title='Welcome', message='Welcome!')
            login_gui()
            dev.destroy()
        else : 
            tk.messagebox.showerror(message='Error, your password is wrong, please try again!')

    login_btn = tk.Button(dev, text="login", command=check123)
    login_btn.place(x=300, y=40)

test_page_btn = tk.Button(win, text="Developer", command=developer_mode)
test_page_btn.place(x=360, y=260)

win.mainloop()

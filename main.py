import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
from tkinter.constants import ANCHOR, S, TOP, X
from tkinter import *
from matplotlib.pyplot import get
# from typing_extensions import Self
import serial
import os
import PIL.ImageGrab as ImageGrab
from http_request import backend_connenct
import json
from datetime import datetime

connector = backend_connenct()
SerialIn = serial.Serial('COM8', 9600, timeout=0.1) #bytesize=serial.EIGHTBITS
SerialIn2 = serial.Serial('COM10', 9600, timeout=0.1)

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
var_usr_name.set('admin')
entry_usr_name = tk.Entry(win, textvariable=var_usr_name)
# entry_usr_name = tk.Entry(win)
entry_usr_name.place(x=130, y=150)
var_usr_pwd = tk.StringVar()
var_usr_pwd.set('admin')
entry_usr_pwd = tk.Entry(win, textvariable=var_usr_pwd, show='*')
# entry_usr_pwd = tk.Entry(win, show='*')
entry_usr_pwd.place(x=130, y=190)
# data_dict = {"data": []}
data_list = []
data_order = [0,1,2,3,16,4,5,6,7,17,8,9,10,11,18,12,13,14,15,19,20,21,22,23,24]

seat_map = {}
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
    login_res = connector.login_server(email=usr_name, password=usr_pwd)
    if login_res:
        print("登入成功!")
    else:
        print("登入失敗!")

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
    sensor1 = mycanvas.create_rectangle(0, 0, 100, 100, fill="white")
    sensor2 = mycanvas.create_rectangle(100, 0, 200, 100, fill="white")
    sensor3 = mycanvas.create_rectangle(200, 0, 300, 100, fill="white")
    sensor4 = mycanvas.create_rectangle(300, 0, 400, 100, fill="white")
    sensor5 = mycanvas.create_rectangle(0, 100, 100, 200, fill="white")
    sensor6 = mycanvas.create_rectangle(100, 100, 200, 200, fill="white")
    sensor7 = mycanvas.create_rectangle(200, 100, 300, 200, fill="white")
    sensor8 = mycanvas.create_rectangle(300, 100, 400, 200, fill="white")
    sensor9 = mycanvas.create_rectangle(0, 200, 100, 300, fill="white")
    sensor10 = mycanvas.create_rectangle(100, 200, 200, 300, fill="white")
    sensor11 = mycanvas.create_rectangle(200, 200, 300, 300, fill="white")
    sensor12 = mycanvas.create_rectangle(300, 200, 400, 300, fill="white")
    sensor13 = mycanvas.create_rectangle(0, 300, 100, 400, fill="white")
    sensor14 = mycanvas.create_rectangle(100, 300, 200, 400, fill="white")
    sensor15 = mycanvas.create_rectangle(200, 300, 300, 400, fill="white")
    sensor16 = mycanvas.create_rectangle(300, 300, 400, 400, fill="white")

    #最右排*4格
    sensor17 = mycanvas.create_rectangle(400, 0, 500, 100, fill="white")
    sensor18 = mycanvas.create_rectangle(400, 100, 500, 200, fill="white")
    sensor19 = mycanvas.create_rectangle(400, 200, 500, 300, fill="white")
    sensor20 = mycanvas.create_rectangle(400, 300, 500, 400, fill="white")

    #最下排*5格
    sensor21 = mycanvas.create_rectangle(0, 400, 100, 500, fill="white")
    sensor22 = mycanvas.create_rectangle(100, 400, 200, 500, fill="white")
    sensor23 = mycanvas.create_rectangle(200, 400, 300, 500, fill="white")
    sensor24 = mycanvas.create_rectangle(300, 400, 400, 500, fill="white")
    sensor25 = mycanvas.create_rectangle(400, 400, 500, 500, fill="white")

    timming = tk.Label(gui, text="Timer : ", font="Arial 18", width=5)
    timming.place(x=395, y=530)
    timer_lb = tk.Label(gui, text="0 s", font="Arial 18", width=4)
    timer_lb.place(x=470, y=530)

    def get_data_name():
        data_name = open("data_name.txt", "r").read().split(",")
        return data_name

    #Start, Stop 連續顯示顏色並暫停
    def btn_color_continuously():
        if running :
            SerialIn.write('s'.encode())                                  #字元s與Arduino-Mega#1溝通
            response = SerialIn.readall()
            value = [int(i.decode("utf-8")) for i in response.split()]

            SerialIn2.write('h'.encode())                                 #字元h與Arduino-Mega#2溝通
            response2 = SerialIn2.readall()
            value2 = [int(i.decode("utf-8")) for i in response2.split()]
            
            
            data_dict = {}
            folder_name, file_name, height, weight, gender = get_data_name()
            # data_dict['name'] = file_name[:-4]
            seat = get_seat(cb2.get())
            data_dict['seat_id'] = seat['id']
            data_dict['seat_type'] = seat['seat_type']
            data_dict['time'] = datetime.strftime(datetime.now(), "%Y%m%d %H:%M:%S")
            data_dict['data'] = [(value + value2)[v] for v in data_order]
            data_dict['sit_pos'] = cb.get()
            data_dict['gender'] = gender
            data_dict['height'] = height
            data_dict['weight'] = weight
            data_list.append(data_dict)
            # fp.write(json.dumps([(value + value2)[v] for v in data_order]) + '\n')
            # fp.close()

            if value == []:                                                 #跳過delay時間
                pass    
            else:
                #sensor1
                Sensor1_value = value[0]
                if (Sensor1_value <= 512):                                #如果壓力小於一半，顏色由綠變黃
                    if (Sensor1_value == 0):
                        clr1 = "#00FF00"
                        mycanvas.itemconfig(sensor1, fill=clr1)
                        
                    else:
                        a = int(Sensor1_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                               #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                       #如果壓力值出現個位數數值補0
                            clr1 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor1, fill=clr1)
                        else:
                            clr1 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor1, fill=clr1)
                else:                                                    #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor1_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr1 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor1, fill=clr1)
                    else:
                        clr1 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor1, fill=clr1)

                Sensor1_lb = tk.Label(labframe, text=Sensor1_value, width=5)
                Sensor1_lb.place(x=65, y=10)

                #Sensor2
                Sensor2_value = value[1]
                if (Sensor2_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor2_value == 0):
                        clr2 = "#00FF00"
                        mycanvas.itemconfig(sensor2, fill=clr2)
                    else:
                        a = int(Sensor2_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr2 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor2, fill=clr2)
                        else:
                            clr2 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor2, fill=clr2)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor2_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr2 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor2, fill=clr2)
                    else:
                        clr2 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor2, fill=clr2)

                Sensor2_lb = tk.Label(labframe, text=Sensor2_value, width=5)
                Sensor2_lb.place(x=65, y=40)

                #Sensor3
                Sensor3_value = value[2]
                if (Sensor3_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor3_value == 0):
                        clr3 = "#00FF00"
                        mycanvas.itemconfig(sensor3, fill=clr3)
                    else:
                        a = int(Sensor3_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr3 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor3, fill=clr3)
                        else:
                            clr3 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor3, fill=clr3)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor3_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr3 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor3, fill=clr3)
                    else:
                        clr3 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor3, fill=clr3)

                Sensor3_lb = tk.Label(labframe, text=Sensor3_value, width=5)
                Sensor3_lb.place(x=65, y=70)

                #Sensor4
                Sensor4_value = value[3]
                if (Sensor4_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor4_value == 0):
                        clr4 = "#00FF00"
                        mycanvas.itemconfig(sensor4, fill=clr4)
                    else:
                        a = int(Sensor4_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr4 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor4, fill=clr4)
                        else:
                            clr4 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor4, fill=clr4)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor4_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr4 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor4, fill=clr4)
                    else:
                        clr4 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor4, fill=clr4)

                Sensor4_lb = tk.Label(labframe, text=Sensor4_value, width=5)
                Sensor4_lb.place(x=65, y=100)

                #Sensor5
                Sensor5_value = value[4]
                if (Sensor5_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor5_value == 0):
                        clr5 = "#00FF00"
                        mycanvas.itemconfig(sensor5, fill=clr5)
                    else:
                        a = int(Sensor5_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr5 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor5, fill=clr5)
                        else:
                            clr5 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor5, fill=clr5)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor5_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr5 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor5, fill=clr5)
                    else:
                        clr5 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor5, fill=clr5)

                Sensor5_lb = tk.Label(labframe, text=Sensor5_value, width=5)
                Sensor5_lb.place(x=65, y=130)

                #Sensor6
                Sensor6_value = value[5]
                if (Sensor6_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor6_value == 0):
                        clr6 = "#00FF00"
                        mycanvas.itemconfig(sensor6, fill=clr6)
                    else:
                        a = int(Sensor6_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr6 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor6, fill=clr6)
                        else:
                            clr6 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor6, fill=clr6)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor6_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr6 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor6, fill=clr6)
                    else:
                        clr6 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor6, fill=clr6)

                Sensor6_lb = tk.Label(labframe, text=Sensor6_value, width=5)
                Sensor6_lb.place(x=65, y=160)

                #Sensor7
                Sensor7_value = value[6]
                if (Sensor7_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor7_value == 0):
                        clr7 = "#00FF00"
                        mycanvas.itemconfig(sensor7, fill=clr7)
                    else:
                        a = int(Sensor7_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr7 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor7, fill=clr7)
                        else:
                            clr7 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor7, fill=clr7)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor7_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr7 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor7, fill=clr7)
                    else:
                        clr7 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor7, fill=clr7)

                Sensor7_lb = tk.Label(labframe, text=Sensor7_value, width=5)
                Sensor7_lb.place(x=65, y=190)

                #Sensor8
                Sensor8_value = value[7]
                if (Sensor8_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor8_value == 0):
                        clr8 = "#00FF00"
                        mycanvas.itemconfig(sensor8, fill=clr8)
                    else:
                        a = int(Sensor8_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr8 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor8, fill=clr8)
                        else:
                            clr8 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor8, fill=clr8)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor8_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr8 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor8, fill=clr8)
                    else:
                        clr8 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor8, fill=clr8)

                Sensor8_lb = tk.Label(labframe, text=Sensor8_value, width=5)
                Sensor8_lb.place(x=65, y=220)

                #Sensor9
                Sensor9_value = value[8]
                if (Sensor9_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor9_value == 0):
                        clr9 = "#00FF00"
                        mycanvas.itemconfig(sensor9, fill=clr9)
                    else:
                        a = int(Sensor9_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr9 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor9, fill=clr9)
                        else:
                            clr9 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor9, fill=clr9)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor9_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr9 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor9, fill=clr9)
                    else:
                        clr9 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor9, fill=clr9)

                Sensor9_lb = tk.Label(labframe, text=Sensor9_value, width=5)
                Sensor9_lb.place(x=65, y=250)

                #Sensor10
                Sensor10_value = value[9]
                if (Sensor10_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor10_value == 0):
                        clr10 = "#00FF00"
                        mycanvas.itemconfig(sensor10, fill=clr10)
                    else:
                        a = int(Sensor10_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr10 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor10, fill=clr10)
                        else:
                            clr10 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor10, fill=clr10)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor10_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr10 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor10, fill=clr10)
                    else:
                        clr10 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor10, fill=clr10)

                Sensor10_lb = tk.Label(labframe, text=Sensor10_value, width=5)
                Sensor10_lb.place(x=65, y=280)

                #Sensor11
                Sensor11_value = value[10]
                if (Sensor11_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor11_value == 0):
                        clr11 = "#00FF00"
                        mycanvas.itemconfig(sensor11, fill=clr11)
                    else:
                        a = int(Sensor11_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr11 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor11, fill=clr11)
                        else:
                            clr11 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor11, fill=clr11)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor11_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr11 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor11, fill=clr11)
                    else:
                        clr11 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor11, fill=clr11)

                Sensor11_lb = tk.Label(labframe, text=Sensor11_value, width=5)
                Sensor11_lb.place(x=65, y=310)

                #Sensor12
                Sensor12_value = value[11]
                if (Sensor12_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor12_value == 0):
                        clr12 = "#00FF00"
                        mycanvas.itemconfig(sensor12, fill=clr12)
                    else:
                        a = int(Sensor12_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr12 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor12, fill=clr12)
                        else:
                            clr12 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor12, fill=clr12)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor12_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr12 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor12, fill=clr12)
                    else:
                        clr12 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor12, fill=clr12)

                Sensor12_lb = tk.Label(labframe, text=Sensor12_value, width=5)
                Sensor12_lb.place(x=65, y=340)

                #Sensor13
                Sensor13_value = value[12]
                if (Sensor13_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor13_value == 0):
                        clr13 = "#00FF00"
                        mycanvas.itemconfig(sensor13, fill=clr13)
                    else:
                        a = int(Sensor13_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr13 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor13, fill=clr13)
                        else:
                            clr13 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor13, fill=clr13)
                else:                                                     #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor13_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr13 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor13, fill=clr13)
                    else:
                        clr13 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor13, fill=clr13)

                Sensor13_lb = tk.Label(labframe, text=Sensor13_value, width=5)
                Sensor13_lb.place(x=65, y=370)

                #Sensor14
                Sensor14_value = value[13]
                if (Sensor14_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor14_value == 0):
                        clr14 = "#00FF00"
                        mycanvas.itemconfig(sensor14, fill=clr14)
                    else:
                        a = int(Sensor14_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr14 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor14, fill=clr14)
                        else:
                            clr14 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor14, fill=clr14)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor14_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr14 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor14, fill=clr14)
                    else:
                        clr14 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor14, fill=clr14)

                Sensor14_lb = tk.Label(labframe, text=Sensor14_value, width=5)
                Sensor14_lb.place(x=65, y=400)

                #Sensor15
                Sensor15_value = value[14]
                if (Sensor15_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor15_value == 0):
                        clr15 = "#00FF00"
                        mycanvas.itemconfig(sensor15, fill=clr15)
                    else:
                        a = int(Sensor15_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr15 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor15, fill=clr15)
                        else:
                            clr15 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor15, fill=clr15)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor15_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr15 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor15, fill=clr15)
                    else:
                        clr15 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor15, fill=clr15)

                Sensor15_lb = tk.Label(labframe, text=Sensor15_value, width=5)
                Sensor15_lb.place(x=65, y=430)

                #Sensor16
                Sensor16_value = value[15]
                if (Sensor16_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor16_value == 0):
                        clr16 = "#00FF00"
                        mycanvas.itemconfig(sensor16, fill=clr16)
                    else:
                        a = int(Sensor16_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr16 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor16, fill=clr16)
                        else:
                            clr16 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor16, fill=clr16)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor16_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr16 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor16, fill=clr16)
                    else:
                        clr16 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor16, fill=clr16)

                Sensor16_lb = tk.Label(labframe, text=Sensor16_value, width=5)
                Sensor16_lb.place(x=65, y=460)

                #Sensor17
                Sensor17_value = value2[0]
                if (Sensor17_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor17_value == 0):
                        clr17 = "#00FF00"
                        mycanvas.itemconfig(sensor17, fill=clr17)
                    else:
                        a = int(Sensor17_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr17 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor17, fill=clr17)
                        else:
                            clr17 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor17, fill=clr17)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor17_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr17 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor17, fill=clr17)
                    else:
                        clr17 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor17, fill=clr17)

                Sensor17_lb = tk.Label(labframe, text=Sensor17_value, width=5)
                Sensor17_lb.place(x=65, y=490)


                #Sensor18
                Sensor18_value = value2[1]
                if (Sensor18_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor18_value == 0):
                        clr18 = "#00FF00"
                        mycanvas.itemconfig(sensor18, fill=clr18)
                    else:
                        a = int(Sensor18_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr18 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor18, fill=clr18)
                        else:
                            clr18 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor18, fill=clr18)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor18_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr18 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor18, fill=clr18)
                    else:
                        clr18 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor18, fill=clr18)

                Sensor18_lb = tk.Label(labframe, text=Sensor18_value, width=5)
                Sensor18_lb.place(x=65, y=520)

                #Sensor19
                Sensor19_value = value2[2]
                if (Sensor19_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor19_value == 0):
                        clr19 = "#00FF00"
                        mycanvas.itemconfig(sensor19, fill=clr19)
                    else:
                        a = int(Sensor19_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr19 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor19, fill=clr19)
                        else:
                            clr19 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor19, fill=clr19)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor19_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr19 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor19, fill=clr19)
                    else:
                        clr19 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor19, fill=clr19)

                Sensor19_lb = tk.Label(labframe, text=Sensor19_value, width=5)
                Sensor19_lb.place(x=65, y=550)

                #Sensor20
                Sensor20_value = value2[3]
                if (Sensor20_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor20_value == 0):
                        clr20 = "#00FF00"
                        mycanvas.itemconfig(sensor20, fill=clr20)
                    else:
                        a = int(Sensor20_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr20 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor20, fill=clr20)
                        else:
                            clr20 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor20, fill=clr20)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor20_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr20 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor20, fill=clr20)
                    else:
                        clr20 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor20, fill=clr20)

                Sensor20_lb = tk.Label(labframe, text=Sensor20_value, width=5)
                Sensor20_lb.place(x=65, y=580)

                #Sensor21
                Sensor21_value = value2[4]
                if (Sensor21_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor21_value == 0):
                        clr21 = "#00FF00"
                        mycanvas.itemconfig(sensor21, fill=clr21)
                    else:
                        a = int(Sensor21_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr21 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor21, fill=clr21)
                        else:
                            clr21 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor21, fill=clr21)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor21_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr21 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor21, fill=clr21)
                    else:
                        clr21 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor21, fill=clr21)

                Sensor21_lb = tk.Label(labframe, text=Sensor21_value, width=5)
                Sensor21_lb.place(x=65, y=610)

                #Sensor22
                Sensor22_value = value2[5]
                if (Sensor22_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor22_value == 0):
                        clr22 = "#00FF00"
                        mycanvas.itemconfig(sensor22, fill=clr22)
                    else:
                        a = int(Sensor22_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr22 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor22, fill=clr22)
                        else:
                            clr22 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor22, fill=clr22)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor22_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr22 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor22, fill=clr22)
                    else:
                        clr22 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor22, fill=clr22)

                Sensor22_lb = tk.Label(labframe, text=Sensor22_value, width=5)
                Sensor22_lb.place(x=65, y=640)

                #Sensor23
                Sensor23_value = value2[6]
                if (Sensor23_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor23_value == 0):
                        clr23 = "#00FF00"
                        mycanvas.itemconfig(sensor23, fill=clr23)
                    else:
                        a = int(Sensor23_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr23 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor23, fill=clr23)
                        else:
                            clr23 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor23, fill=clr23)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor23_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr23 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor23, fill=clr23)
                    else:
                        clr23 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor23, fill=clr23)

                Sensor23_lb = tk.Label(labframe, text=Sensor23_value, width=5)
                Sensor23_lb.place(x=65, y=670)

                #Sensor24
                Sensor24_value = value2[7]
                if (Sensor24_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor24_value == 0):
                        clr24 = "#00FF00"
                        mycanvas.itemconfig(sensor24, fill=clr24)
                    else:
                        a = int(Sensor24_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr24 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor24, fill=clr24)
                        else:
                            clr24 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor24, fill=clr24)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor24_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr24 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor24, fill=clr24)
                    else:
                        clr24 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor24, fill=clr24)

                Sensor24_lb = tk.Label(labframe, text=Sensor24_value, width=5)
                Sensor24_lb.place(x=65, y=700)

                #Sensor25
                Sensor25_value = value2[8]
                if (Sensor25_value <= 512):                                 #如果壓力小於一半，顏色由綠變黃
                    if (Sensor25_value == 0):
                        clr25 = "#00FF00"
                        mycanvas.itemconfig(sensor25, fill=clr25)
                    else:
                        a = int(Sensor25_value *0.49)
                        low_16 = hex(a)[2:]
                        rr = int('10', 16)                                #16進制'F'的下一進位
                        if (int(low_16, 16) < rr):                        #如果壓力值出現個位數數值補0
                            clr25 = "#0"+low_16+"FF00"
                            mycanvas.itemconfig(sensor25, fill=clr25)
                        else:
                            clr25 = "#"+low_16+"FF00"
                            mycanvas.itemconfig(sensor25, fill=clr25)
                else:                                                  #如果壓力大於一半，顏色由黃變紅
                    b = int((Sensor25_value - 512)*0.49)
                    max_value = int('FF', 16)
                    min_value = int (str(hex(b)[2:]), 16)
                    summary = max_value - min_value
                    high_16 = hex(summary)[2:]
                    rr = int('10', 16)
                    if (int(high_16, 16) < rr):
                        clr25 = "#FF0"+high_16+"00"
                        mycanvas.itemconfig(sensor25, fill=clr25)
                    else:
                        clr25 = "#FF"+high_16+"00"
                        mycanvas.itemconfig(sensor25, fill=clr25)

                Sensor25_lb = tk.Label(labframe, text=Sensor25_value, width=5)
                Sensor25_lb.place(x=65, y=730)
            
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
        folder_name, file_name, height, weight, gender = get_data_name()
        data_json = {}
        data_json['name'] = file_name[:-4]
        data_json['data'] = data_list
        json_file = open(os.path.join(folder_name, f"{data_json['name']}.json"), "w+", encoding="utf-8")
        json.dump(data_list, json_file, indent=1, ensure_ascii=False)
        # json_file = open("%s/json.txt" %folder_name, "a+")
        # json_file.write(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")+"\n"+str(data_json)+"\n")
        # json_file.close

        # json_file2 = open("sample_data2.json", "a+")
        # json_file2.write(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")+"\n"+data_json+"\n")
        # json_file2.close 
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
            data_name = open("data_name.txt", "r").read()
            data_name = data_name.split(",")
            folder_name = data_name[0]
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
        mycanvas.itemconfig(sensor1, fill="white")
        mycanvas.itemconfig(sensor2, fill="white")
        mycanvas.itemconfig(sensor3, fill="white")
        mycanvas.itemconfig(sensor4, fill="white")
        mycanvas.itemconfig(sensor5, fill="white")
        mycanvas.itemconfig(sensor6, fill="white")
        mycanvas.itemconfig(sensor7, fill="white")
        mycanvas.itemconfig(sensor8, fill="white")
        mycanvas.itemconfig(sensor9, fill="white")
        mycanvas.itemconfig(sensor10, fill="white")
        mycanvas.itemconfig(sensor11, fill="white")
        mycanvas.itemconfig(sensor12, fill="white")
        mycanvas.itemconfig(sensor13, fill="white")
        mycanvas.itemconfig(sensor14, fill="white")
        mycanvas.itemconfig(sensor15, fill="white")
        mycanvas.itemconfig(sensor16, fill="white")
        mycanvas.itemconfig(sensor17, fill="white")
        mycanvas.itemconfig(sensor18, fill="white")
        mycanvas.itemconfig(sensor19, fill="white")
        mycanvas.itemconfig(sensor20, fill="white")
        mycanvas.itemconfig(sensor21, fill="white")
        mycanvas.itemconfig(sensor22, fill="white")
        mycanvas.itemconfig(sensor23, fill="white")
        mycanvas.itemconfig(sensor24, fill="white")
        mycanvas.itemconfig(sensor25, fill="white")
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

                                                                                                                                                                            
    def get_user_seat_list() -> list:
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
        data_name = open("data_name.txt", "r").read()
        data_name = data_name.split(",")
        folder_name = data_name[0]
        fp = open("%s/Status.txt" %(folder_name), "a+")
        fp.write(status_name)
        fp.write("\n")
        fp.close()

        

    Label2 = tk.Label(gui, text="File : ", font="Arial 12")
    Label2.place(x=120, y=580)

    Label3 = tk.Label(gui, text="Status : ", font="Arial 12")
    Label3.place(x=120, y=640)

    Label4 = tk.Label(gui, text="Select : ", font="Arial 12")
    Label4.place(x=120, y=700)
    

    # (1)坐姿-正 (2)坐姿-偏左 (3)坐姿-偏右 (4)坐姿-翹右腳 (5)坐姿-翹左腳 (6)坐姿-翹右二郎腿 
    # (7)坐姿-翹左二郎腿  (8)後仰
    cb = ttk.Combobox(gui, value=["1", "2", "3", "4", "5", 
                                    "6", "7", "8"], width=16, state="readonly")
    cb.current(0)
    cb.place(x=180, y=640)

    
    cb2 = ttk.Combobox(gui, value=get_user_seat_list(), width=16, state="readonly")
    cb2.current(0)
    cb2.place(x=180, y=700)

    def output():
        seat = get_seat(cb2.get())
        print(seat)
        print(seat['id'])

    # bt3 = tk.Button(gui, text="output", command=output)
    # bt3.place(x=325, y=695)

    # save_btn = tk.Button(gui, text="Save", command=save)
    # save_btn.place(x=325, y=635)

    # json_btn = tk.Button(gui, text="Process", command=get_json)
    # json_btn.place(x=370, y=635)

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
    
    ########顯示標籤############################################
    labframe = LabelFrame(gui, text="Sensor value", font="Arial 12", labelanchor=N)
    labframe.place(x=550, y=15, height=780, width=130)
    lb1 = tk.Label(labframe, text='Sensor1 : ')
    lb1.place(x=5, y=10)
    lb2 = tk.Label(labframe, text='Sensor2 : ')
    lb2.place(x=5, y=40)    
    lb3 = tk.Label(labframe, text='Sensor3 : ')
    lb3.place(x=5, y=70) 
    lb4 = tk.Label(labframe, text='Sensor4 : ')
    lb4.place(x=5, y=100) 
    lb5 = tk.Label(labframe, text='Sensor5 : ')
    lb5.place(x=5, y=130)
    lb6 = tk.Label(labframe, text='Sensor6 : ')
    lb6.place(x=5, y=160)
    lb7 = tk.Label(labframe, text='Sensor7 : ')
    lb7.place(x=5, y=190)
    lb8 = tk.Label(labframe, text='Sensor8 : ')
    lb8.place(x=5, y=220)    
    lb9 = tk.Label(labframe, text='Sensor9 : ')
    lb9.place(x=5, y=250)
    lb10 = tk.Label(labframe, text='Sensor10 : ')
    lb10.place(x=5, y=280)
    lb11 = tk.Label(labframe, text='Sensor11 : ')
    lb11.place(x=5, y=310)
    lb12 = tk.Label(labframe, text='Sensor12 : ')
    lb12.place(x=5, y=340)    
    lb13 = tk.Label(labframe, text='Sensor13 : ')
    lb13.place(x=5, y=370) 
    lb14 = tk.Label(labframe, text='Sensor14 : ')
    lb14.place(x=5, y=400) 
    lb15 = tk.Label(labframe, text='Sensor15 : ')
    lb15.place(x=5, y=430)
    lb16 = tk.Label(labframe, text='Sensor16 : ')
    lb16.place(x=5, y=460)
    lb17 = tk.Label(labframe, text='Sensor17 : ')
    lb17.place(x=5, y=490)
    lb18 = tk.Label(labframe, text='Sensor18 : ')
    lb18.place(x=5, y=520)  
    lb19 = tk.Label(labframe, text='Sensor19 : ')
    lb19.place(x=5, y=550)  
    lb20 = tk.Label(labframe, text='Sensor20 : ')
    lb20.place(x=5, y=580)  
    lb21 = tk.Label(labframe, text='Sensor21 : ')
    lb21.place(x=5, y=610)  
    lb22 = tk.Label(labframe, text='Sensor22 : ')
    lb22.place(x=5, y=640)  
    lb23 = tk.Label(labframe, text='Sensor23 : ')
    lb23.place(x=5, y=670)  
    lb24 = tk.Label(labframe, text='Sensor24 : ')
    lb24.place(x=5, y=700)  
    lb25 = tk.Label(labframe, text='Sensor25 : ')
    lb25.place(x=5, y=730)    
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
btn_login = tk.Button(win, text='Login', command=usr_login)
btn_login.place(x=100, y=230)
btn_sign_up = tk.Button(win, text='Sign up', command=usr_sign_up)
btn_sign_up.place(x=200, y=230)


win.mainloop()
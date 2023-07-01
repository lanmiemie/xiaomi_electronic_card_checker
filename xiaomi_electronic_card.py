import io
import re
from tkinter import *
import tkinter.ttk
import os
from PIL import Image, ImageTk
import tkinter.messagebox
import webbrowser
import requests
import sys
import base64
import time
from lxml import etree
from favicon import img
import tkinter.filedialog
from tkinter import scrolledtext
from fake_useragent import FakeUserAgent
import hashlib
from xiaomiapi import *

root = Tk()
#root.attributes("-alpha", 0.8)
ver = "1.1.0"
title='小米电子保卡查询 - 测试版 '+ver
root.title(title)
tmp = open("favicon.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
global tmpico
tmpico = ImageTk.PhotoImage(file="favicon.ico")
root.iconphoto(False ,tmpico)
os.remove("favicon.ico")
#root.iconbitmap(".\\backup_user\du.ico")
winWidth = 345
winHeight = 310
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
root.resizable(0,0)
port = StringVar()
VC_WARRANTY_TOKEN = ''
data_stream = ''
UUID = ''

lvalue = StringVar()
lvalue.set("变量值")

timeleftvalue = StringVar()
timeleftvalue.set("距离保修过期还有: 000 天")

main_menu = Menu(root)
root.config (menu=main_menu)

def loading_captcha():
    try:
        html = requests.get("https://chat.kefu.mi.com")
    except Exception as e:
        tkinter.messagebox.showerror(title='失败',message='网络连接失败\n您可以通过以下操作来帮助您排除网络问题\n\n1. 如果您打开了代理（Clash,Socks), 请将它关闭.\n2.检查网络是否通畅.\n3.检查路由器等设施是否正确连接到互联网.\n4.您压根没有连接到互联网.')
        return 0
    global VC_WARRANTY_TOKEN,data_stream,UUID
    VC_WARRANTY_TOKEN,data_stream = get_captcha_image()
    UUID = get_activation_uuid()
    pil_image = Image.open(data_stream)
    global tk_image
    tk_image = ImageTk.PhotoImage(pil_image)
    label_captcha.config(image=tk_image)
    label_captcha.image=tk_image
    label_captcha.pack(fill=BOTH, expand='yes')

def check_code(mode):
        if len(inp1.get()) == 0 and len(inp2.get()) == 0: 
            tkinter.messagebox.showerror(title='错误', message="哦吼！！您似乎啥也没输入？，请再试一次")
            return 0
        if len(inp1.get()) == 0: 
            tkinter.messagebox.showerror(title='错误', message="哦吼！！您似乎没输入设备串号？，请再试一次")
            return 0
        if len(inp2.get()) == 0: 
            tkinter.messagebox.showerror(title='错误', message="哦吼！！您似乎没输入验证码？，请再试一次")
            return 0
        
        if mode == 'repair':
            key = inp1.get().replace("\n", "").upper()
            captcha_code = inp2.get().replace("\n", "")
            post_device_info(key,captcha_code)
        elif  mode == 'activation':
            key = inp1.get().replace("\n", "").upper()
            post_device_info(key,captcha_code)
        else:
            tkinter.messagebox.showerror(title='错误', message="未知指令")

def backcheckbutton_loading_captcha():
    try:
        html = requests.get("https://chat.kefu.mi.com")
    except Exception as e:
        tkinter.messagebox.showerror(title='失败',message='网络连接失败\n您可以通过以下操作来帮助您排除网络问题\n\n1. 如果您打开了代理（Clash,Socks), 请将它关闭.\n2.检查网络是否通畅.\n3.检查路由器等设施是否正确连接到互联网.\n4.您压根没有连接到互联网.')
        return 0
    loading_captcha()

def post_device_info(key,captcha_code):
    try:
        html = requests.get("https://chat.kefu.mi.com")
    except Exception as e:
        tkinter.messagebox.showerror(title='失败',message='网络连接失败\n您可以通过以下操作来帮助您排除网络问题\n\n1. 如果您打开了代理（Clash,Socks), 请将它关闭.\n2.检查网络是否通畅.\n3.检查路由器等设施是否正确连接到互联网.\n4.您压根没有连接到互联网.')
        return 0
    
    try:
        get_state, repair_state, get_msg, all_info, timeleft, repair_end = get_activation_info(VC_WARRANTY_TOKEN, UUID, key, captcha_code)
    except Exception as e:
        tkinter.messagebox.showerror(title='失败',message='未知错误\n请检查 SN 或 IMEI 码 输入是否正确?')
        return 0 
    if get_state == '200':
        root.withdraw()
        top_for_repair = Toplevel()
        title='查询成功'
        top_for_repair.title(title)
        tmp = open("favicon.ico","wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        global tmpico
        tmpico = ImageTk.PhotoImage(file="favicon.ico")
        top_for_repair.iconphoto(False ,tmpico)
        os.remove("favicon.ico")
        #root.iconbitmap(".\\backup_user\du.ico")
        winWidth = 345
        winHeight = 310
        screenWidth = top_for_repair.winfo_screenwidth()
        screenHeight = top_for_repair.winfo_screenheight()
        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)
        top_for_repair.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        top_for_repair.resizable(0,0)

        def on_closing():
            backcheckbutton_loading_captcha()
            top_for_repair.destroy()
            root.wm_deiconify()

        top_for_repair.protocol("WM_DELETE_WINDOW", on_closing)

        backcheckbutton = tkinter.ttk.Button(top_for_repair,text="重新查询",command=lambda:on_closing())
        full_device_info_lf = tkinter.ttk.LabelFrame(top_for_repair,text="详细信息")
        curt_device_info_lf = tkinter.ttk.LabelFrame(top_for_repair,text="保修状态")
        timeleft_device_info_label = tkinter.ttk.Label(curt_device_info_lf,textvariable=timeleftvalue,foreground="black",font=("黑体", 12))
        curt_device_info_label = tkinter.ttk.Label(curt_device_info_lf,textvariable=lvalue,font=("黑体", 30))
        full_device_info_text = scrolledtext.ScrolledText(full_device_info_lf, font=('Consolas', 10))

        full_device_info_text.config(state=NORMAL)
        full_device_info_lf.place(x=8, y=155,width=200,height=150)
        full_device_info_text.pack(fill=BOTH, expand='yes')
        curt_device_info_lf.place(x=8, y=8,width=330,height=145)
        curt_device_info_label.pack(anchor=CENTER, expand='yes')
        timeleft_device_info_label.pack(anchor=S)
        backcheckbutton.place(x=235,y=220)

        if timeleft == "未知":
            finally_timeleft = '距离保修过期还有: {}'.format(timeleft)
        elif  timeleft == 0:
            finally_timeleft = '该设备的保修已过期'
        else:
            finally_timeleft = '距离保修过期还有: {} 天'.format(timeleft)

        if repair_state == '已失效':
            curt_device_info_label.config(foreground="red")
        elif repair_state == '未失效':
            curt_device_info_label.config(foreground="green")
        else:
            curt_device_info_label.config(foreground="black")

        lvalue.set(repair_state)
        timeleftvalue.set(finally_timeleft)
        full_device_info_text.delete("1.0","end")
        full_device_info_text.insert("end", all_info)
        full_device_info_text.config(state=DISABLED)
    else:
        tkinter.messagebox.showerror(title='失败',message=get_msg)
        loading_captcha()

lf1 = tkinter.ttk.LabelFrame(root,text="设备信息")
lf1.place(x=8, y=8,width=330,height=150)

captcha_lf = tkinter.ttk.LabelFrame(lf1,text="验证码")
captcha_lf.place(x=175,y=55,width=120,height=70)
label_captcha = Label(captcha_lf, bg='white')

Label(lf1, text="设备串号").place(x=20,y=30)
inp1 = tkinter.ttk.Entry(lf1,textvariable = port,width=27)
inp1.place(x=100, y=30)
Label(lf1, text="验证码").place(x=30,y=80)
inp2 = tkinter.ttk.Entry(lf1,width=8)
port.set('S/N 或 IMEI')
inp2.place(x=100, y=80)

#main_menu.add_command(label="查询设备激活锁状态")#, command = lambda:qrcode_login(mode='QRCODE'))

loading_captcha()

postbutton = tkinter.ttk.Button(root,text="立即查询", command = lambda:check_code(mode='repair'))
postbutton.place(x=125,y=200)

root.mainloop()
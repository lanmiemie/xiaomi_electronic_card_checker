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
ver = "1.0.0"
title='小米电子保卡查询 - 测试版 '+ver
root.title(title)
tmp = open("xueanquan.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
global tmpico
tmpico = ImageTk.PhotoImage(file="xueanquan.ico")
root.iconphoto(False ,tmpico)
os.remove("xueanquan.ico")
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

full_device_info_lf = tkinter.ttk.LabelFrame(root,text="详细信息")
full_device_info_lf.place(x=8, y=155,width=200,height=150)

full_device_info_text = scrolledtext.ScrolledText(full_device_info_lf, font=('Consolas', 8))
full_device_info_text.pack(fill=BOTH, expand='yes')

curt_device_info_lf = tkinter.ttk.LabelFrame(root,text="保修状态")
curt_device_info_lf.place(x=8, y=8,width=330,height=145)

lvalue = StringVar()
lvalue.set("变量值")

timeleftvalue = StringVar()
timeleftvalue.set("距离保修过期还有: 000 天")

curt_device_info_label = tkinter.ttk.Label(curt_device_info_lf,textvariable=lvalue,foreground="green",font=("黑体", 30))
curt_device_info_label.pack(anchor=CENTER, expand='yes')

timeleft_device_info_label = tkinter.ttk.Label(curt_device_info_lf,textvariable=timeleftvalue,foreground="black",font=("黑体", 12))
timeleft_device_info_label.pack(anchor=S)

backcheckbutton = tkinter.ttk.Button(root,text="重新查询")
backcheckbutton.place(x=235,y=220)

root.mainloop()
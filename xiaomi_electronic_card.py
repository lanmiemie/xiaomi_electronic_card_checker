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
from xiaomiapi import get_captcha_image

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

lf1 = tkinter.ttk.LabelFrame(root,text="设备信息")
lf1.place(x=8, y=8,width=330,height=150)

Label(lf1, text="教师账号").place(x=40,y=30)
inp1 = Entry(lf1, relief=GROOVE)
inp1.place(x=120, y=30)
Label(lf1, text="密码").place(x=50,y=80)
inp2 = Entry(lf1, relief=GROOVE,textvariable = port)
port.set('填写验证码')
inp2.place(x=120, y=80)



root.mainloop()
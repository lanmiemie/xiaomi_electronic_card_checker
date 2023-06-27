# !! - pip install fake_useragent lxml requests
import io
import threading
import time
import webbrowser
import requests
from lxml import etree
import re
import json
from fake_useragent import FakeUserAgent
import datetime

def get_captcha_image():

    url = 'https://chat.kefu.mi.com/api/captcha/getCode?source=electronicCard'

    headers = {'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Accept-Encoding': 'gzip, deflate, br'}
    
    res = requests.get(url=url,headers=headers)
    image_bytes = res.content
    data_stream = io.BytesIO(image_bytes)
    image = open('a.png', 'wb')
    image.write(image_bytes)

    VC_WARRANTY_TOKEN = 'VC_WARRANTY_TOKEN=' + str(re.findall('VC_WARRANTY_TOKEN=(.*?);', str(res.headers['Set-Cookie']))).replace("'",'').replace(']','').replace('[','')
    #print(VC_WARRANTY_TOKEN)

    return VC_WARRANTY_TOKEN,data_stream

def get_activation_uuid():

    url = 'https://chat.kefu.mi.com/page/activation#/'

    
    headers = {'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Accept-Encoding': 'gzip, deflate, br'}
    
    res = requests.get(url=url,headers=headers)

    UUID = 'UUID=' + str(re.findall('UUID=(.*?);', str(res.headers['Set-Cookie']))).replace("'",'').replace(']','').replace('[','')
    #print(UUID)

    return UUID

def get_activation_info(VC_WARRANTY_TOKEN,UUID,key,captcha_code):

    all_info = ' '
    get_msg = ' '
    repair_state = ' '
    timeleft = ' '
    repair_end = ' '

    #key = str(input('SN or IMEI :')).replace(' ','').upper()
    #captcha_code = str(input('VerifyCode :')).replace(' ','')

    cookies = VC_WARRANTY_TOKEN + ';' + UUID

    url = 'https://chat.kefu.mi.com/api/warrantyCard/search?key={0}&verifyCode={1}'.format(key,captcha_code)

    headers = {'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Cookie': cookies,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Accept-Encoding': 'gzip, deflate, br'}
    
    res = requests.get(url=url,headers=headers)

    getjson = json.loads(res.content)
    print(getjson)

    get_state = str(re.findall('"code":(.*?),', str(res.text))).replace("'",'').replace(']','').replace('[','')

    if get_state == '200':
        all_data_info = getjson["data"]
        if all_data_info == None:
            print("S/N 或 IMEI 码输入错误，请再试一次")
            return 0
        else:
            baseinfo = all_data_info["baseInfo"]
            serviceinfo = all_data_info["serviceInfo"]
            #print(all_data_info)
            check_state = '获取成功'
            print(check_state)
            #get_data = str(re.findall('"data":{(.*?)}', str(res.text)))
            goodsname = baseinfo["goodsName"]
            activetime = baseinfo["activeTime"]
            repair_start = serviceinfo["repairStartTime"]
            repair_end = serviceinfo["repairEndTime"]
            timeleft = serviceinfo["timeLeft"]
            if timeleft == 0:
                repair_state = '已失效'
            else:
                repair_state = '未失效'
            get_msg = getjson["msg"]
            all_info = '商品名称:{0}\n激活时间:{1}\n保修开始时间:{2}\n保修结束时间:{3}\n保修状态:{4}\n保修剩余天数:{5}'.format(goodsname,activetime,repair_start,repair_end,repair_state,timeleft)
            #print(all_info)
    else:
        check_state = '获取失败'
        print(check_state)
        get_msg = getjson["msg"]
        print(get_msg)
    
    return get_state,repair_state,get_msg,all_info,timeleft,repair_end

def check_activation_lock(imei):
    # Request
    # GET https://i.mi.com/support/anonymous/status

    try:
        response = requests.get(
            url="https://i.mi.com/support/anonymous/status",
            params={
                "id": imei,
                "ts": int(time.time()*1000) # timestamp added
            },
        )

        all_info = ' '

        getjson = json.loads(response.content)
        print(json.loads(response.content))

        if str('phone') and str('email') in str(response.text):
            print('1')
            info_data = getjson["data"]
            phonenum = str(info_data["phone"]).replace("'",'').replace(']','').replace('[','')
            lock_or_unlock = str(info_data["locked"]).replace("'",'').replace(']','').replace('[','')
            emailnum = str(info_data["email"]).replace("'",'').replace(']','').replace('[','')
            timeStamp = float(getjson["ts"])/1000
            print(timeStamp)
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            all_info = '绑定号码: {0}\n激活锁状态: {1}\n绑定邮箱: {2}\n查询时间: {3}'.format(phonenum,lock_or_unlock,emailnum,otherStyleTime)
            print(all_info)
        elif str('phone') in str(response.text):
            print('2')
            info_data = getjson["data"]
            phonenum = str(info_data["phone"]).replace("'",'').replace(']','').replace('[','')
            lock_or_unlock = str(info_data["locked"]).replace("'",'').replace(']','').replace('[','')
            timeStamp = float(getjson["ts"])/1000
            print(timeStamp)
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            all_info = '绑定号码: {0}\n激活锁状态: {1}\n查询时间: {2}'.format(phonenum,lock_or_unlock,otherStyleTime)
            print(all_info)
        elif str('email') in str(response.text):
            print('3')
            info_data = getjson["data"]
            emailnum = str(info_data["email"]).replace("'",'').replace(']','').replace('[','')
            lock_or_unlock = str(info_data["locked"]).replace("'",'').replace(']','').replace('[','')
            timeStamp = float(getjson["ts"])/1000
            print(timeStamp)
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            all_info = '绑定邮箱: {0}\n激活锁状态: {1}\n查询时间: {2}'.format(emailnum,lock_or_unlock,otherStyleTime)
            print(all_info)
        else:
            print('\n未上锁或是IMEI输入错误 ..')

    except requests.exceptions.RequestException:
        print('\nConnect fail due to some network error ..')

    return all_info

    #print(res.text)



#VC_WARRANTY_TOKEN,data_stream = get_captcha_image()
#UUID = get_activation_uuid()
#get_activation_info(VC_WARRANTY_TOKEN,UUID)

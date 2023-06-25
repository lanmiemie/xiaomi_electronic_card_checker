# !! - pip install fake_useragent lxml requests
import io
import threading
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
    print(VC_WARRANTY_TOKEN)

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
    print(UUID)

    return UUID

def get_activation_info(VC_WARRANTY_TOKEN,UUID):

    key = str(input('SN or IMEI :')).replace(' ','').upper()
    captcha_code = str(input('code :')).replace(' ','')

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
            print('获取成功\n')
            #get_data = str(re.findall('"data":{(.*?)}', str(res.text)))
            goodsname = baseinfo["goodsName"]
            activetime = baseinfo["activeTime"]
            repair_start = serviceinfo["repairStartTime"]
            repair_end = serviceinfo["repairEndTime"]
            timeleft = serviceinfo["timeLeft"]
            repair_state = ' '
            if timeleft == 0:
                repair_state = '已失效'
            else:
                repair_state = '未失效'
            all_info = '商品名称:{0}\n激活时间:{1}\n保修开始时间:{2}\n保修结束时间:{3}\n保修状态:{4}\n保修剩余天数:{5}'.format(goodsname,activetime,repair_start,repair_end,repair_state,timeleft)
            print(all_info)
    else:
        print('获取失败\n')
        get_msg = getjson["msg"]
        print(get_msg)

    #print(res.text)



VC_WARRANTY_TOKEN,data_stream = get_captcha_image()
UUID = get_activation_uuid()
get_activation_info(VC_WARRANTY_TOKEN,UUID)

import re
import requests
import os
import json
import datetime
import time

def send_request(imei):
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
        
        timeStamp = 1557502800/1000
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print(otherStyleTime)

        getjson = json.loads(response.content)
        print(json.loads(response.content))

        if str('phone') and str('email') in str(response.text):
            print('1')
            info_data = getjson["data"]
            phonenum = str(info_data["phone"]).replace("'",'').replace(']','').replace('[','')
            lock_or_unlock = str(info_data["locked"]).replace("'",'').replace(']','').replace('[','')
            if lock_or_unlock == 'True':
                lock_or_unlock = "已上锁"
            elif lock_or_unlock == 'False':
                lock_or_unlock = "未上锁"
            else:
                lock_or_unlock = "Unknown"
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
            if lock_or_unlock == 'True':
                lock_or_unlock = "已上锁"
            elif lock_or_unlock == 'False':
                lock_or_unlock = "未上锁"
            else:
                lock_or_unlock = "Unknown"
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
            if lock_or_unlock == 'True':
                lock_or_unlock = "已上锁"
            elif lock_or_unlock == 'False':
                lock_or_unlock = "未上锁"
            else:
                lock_or_unlock = "Unknown"
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
        

def usage():
    print("\nXiaomi Activation Lock Checker ")
    print("by TwizzyIndy")
    print("2018/7")
    print("\nusage: python mi_activationlock_check.py {IMEI}")
    print("note: IMEI need to be at least 15 digit\n")
    
def main():
    
    if len(os.sys.argv) < 2:
        usage()
        return
    elif len(os.sys.argv[1]) < 15:
        usage()
        
    send_request( os.sys.argv[1] )
    
if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import sys
import socket
import requests
import pymysql
from tmshop import settings



def counter(start_at=0):
    count = [start_at]
    def incr():
        count[0]+=1
        return count[0]
    return incr

def use_proxy(browser,proxy,url):

    profile = browser.profile
    profile.set_preference('network.proxy.type',1)
    profile.set_preference('network.proxy.http', proxy[0])
    profile.set_preference('network.proxy.http_port', int(proxy[1]))
    profile.set_preference('permissions.default.image', 2)
    profile.update_preferences()
    browser.profile=profile
    browser.get(url)
    browser.implicitly_wait(30)
    return browser


class Singleton(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            orig = super(Singleton,cls)
            cls._instance = orig.__new__(cls,*args,**kwargs)
        return cls._instance


class GetIp():
    def __init__(self):

        #获取ip
        sql='SELECT ip,port,type FROM proxy_ip'
        conn,cursor = self.db_conn()
        try:
            cursor.execute(sql)
            self.result = cursor.fetchall()

        except:
            print("no data in database")
        else:
            cursor.close()
            conn.close()

    def db_conn(self):
        database = settings.get('DATABASE')
        conn = pymysql.connect(database)
        cursor = conn.cursor()
        return conn, cursor

    def del_ip(self,record):
        sql="DELETE FROM proxy_ip WHERE ip='%s' AND port ='%s'" %(record[0],record[1])
        print(sql)
        conn, cursor = self.db_conn()
        try:
            cursor.execute(sql)
        except:
            print("error delete --%s --%s" %(record[0],record[1]))
        else:
            cursor.close()
            conn.close()


    def judge_ip(self,record):
        http_url="http://www.baidu.com/"
        https_url="https://www.alipay.com/"
        proxy_type=record[2].lower()
        url=http_url if proxy_type == "http" else https_url
        proxy="%s:%s"%(record[0],record[1])
        try:
            req=requests.get(url=url,proxy=proxy,proxy_type=proxy_type)

        except:
            print("ip error --%s"%url)
            self.del_ip(record)
            return False
        else:
            code = requests.get(url).status_code
            if code >= 200 and code <=300:
                print("Effective proxy ip",record)
                return True
            else:
                print('Error ip',record)
                self.del_ip(record)
                return False

    def get_ips(self):
        print('Proxy getip was runing....')
        http = [h[0:2] for h in self.result if h[2] == 'HTTP' and self.judge_ip(h)]
        https = [h[0:2] for h in self.result if h[2] == 'HTTPS' and self.judge_ip(h)]
        print("HTTP:",len(http),"Https:",len(https))
        return {'http':http,'https':https}
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import base64
import logging
from tmshop.proxy import GetIp

ips = GetIp.get_ips()


class ProxyMiddleware(object):
    #计算http ip个数
    http_n=0
    https_n=0

    def process_request(self,request,spider):

        if request.url.startswith("http://"):
            n=ProxyMiddleware.http_n
            n= n if n<len(ips['http']) else 0
            request.meta['proxy'] = "http://%s:%d"%(
                ips['http'][n][0],int(ips['http'][n][1]))
            logging.info('Squence - http : %s -%s'%(n,str(ips['http'])))
            ProxyMiddleware.http_n=n+1

        if request.url.startswith("https://"):
            n = ProxyMiddleware.https_n
            n = n if n < len(ips['https']) else 0
            request.meta['proxy'] = "https://%s:%d" % (
                ips['https'][n][0], int(ips['https'][n][1]))
            logging.info('Squence - https : %s -%s' % (n, str(ips['http'])))
            ProxyMiddleware.https_n = n + 1








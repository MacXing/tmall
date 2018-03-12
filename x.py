import requests
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
print(requests.get('http://www.xicidaili.com/nn/1',headers=header).status_code)

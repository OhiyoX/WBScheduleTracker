import requests
from requests.exceptions import RequestException
import time
from random import randint


def get_response(url, headers=None):
    """获得网页"""
    # 设置头
    headers_pool = [{
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'},
                    {
                        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55"}
                    ]
    if headers is None:
        headers = headers_pool[randint(0,len(headers_pool)-1)]
    countdown = 0
    while True:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
        except RequestException:
            countdown += 1
            time.sleep(0.5*countdown)
            print('retry')
            if countdown >= 10:
                print("达到重试最大次数")
                return None
def get_time():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

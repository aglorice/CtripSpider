# -*- coding = utf-8 -*-
# @Time :2023/7/13 21:11
# @Author :小岳
# @Email  :401208941@qq.com
# @PROJECT_NAME :scenic_spots_comment
# @File :  proxy.py
import requests

from config import IS_PROXY


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


# your spider code

def my_get_proxy() -> dict:
    if IS_PROXY:
        content = get_proxy()
        while not content.get("https"):
            content = get_proxy()
        proxy = content.get("proxy")
        _proxy = {"http": "http://{}".format(proxy),"https": "http://{}".format(proxy)}
        return _proxy
    else:
        return {}
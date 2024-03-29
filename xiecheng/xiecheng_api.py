import json
import math
import os
import random
import re
import threading
import time

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

from config import IS_VERIFY, TIME_OUT
from utils.fake_user_agent import get_fake_user_agent
from utils.proxy import my_get_proxy
from utils.utils import create_file, jsonFileToDate, dateToJsonFileSceneInfo

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

# 获取热门城市的id(post)
GET_CITY = "https://vacations.ctrip.com/restapi/gateway/14422/genericDestRecommend"

# 携程景区首页(get)
GET_HOME = "https://you.ctrip.com/"

# 携程景区评论(post)
GET_COMMENT = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList"

# 获取景区详细信息(post)
GET_SCENE_INFO = "https://m.ctrip.com/restapi/soa2/18254/json/GetSightOverview"


class XieCheng:
    def __init__(self, console: Console):
        self.scene_list = []
        self.sees = requests.session()
        self.console = console
        self.sees.verify = IS_VERIFY
        self.get_home()

    def get_home(self):
        self.sees.get(
            url=GET_HOME,
            headers={
                "User-Agent": get_fake_user_agent("mobile")
            },
            proxies=my_get_proxy(),
            timeout=TIME_OUT
        )

    def get_areas(self) -> list:
        city_list = []
        try:
            res = self.sees.get(
                url=GET_HOME,
                headers={
                    "User-Agent": get_fake_user_agent("pc")
                },
                proxies=my_get_proxy(),
                timeout=TIME_OUT
            )
        except Exception as e:
            self.console.print(f"[red]获取城市景区信息失败，{e},你可以检查你的网路或者代理。", style="bold red")
            exit()
        res_shop = BeautifulSoup(res.text, "lxml")
        areas = res_shop.find_all("div", attrs={"class": "city-selector-tab-main-city"})

        for area in areas:
            area_title = area.find("div", attrs={"class": "city-selector-tab-main-city-title"}).string
            if area_title is None:
                continue
            area_items = area.find_all("div", attrs={"class": "city-selector-tab-main-city-list"})
            area_items_list = [{"name": item.string, "url": item["href"]} for item in area_items[0].find_all("a")]
            city_list.append({
                "name": area_title,
                "city": area_items_list
            })
        return city_list

    def get_city_scene(self, city_name, city_url: str) -> list:
        """
        获取城市热门景区信息
        :param city_name: 城市名称
        :param city_url: 城市对应在携程的主页yrl
        :return: 该城市的热门景区信息
        """
        self.console.rule(f"[green]正在获取[yellow]{city_name}[/yellow]的景区信息[/green]", characters="*")
        scene_list = []
        try:
            res = self.sees.get(
                url=city_url,
                headers={
                    "User-Agent": get_fake_user_agent("mobile")
                },
                proxies=my_get_proxy(),
                timeout=TIME_OUT
            )
        except Exception as e:
            self.console.print(f"[red]获取城市景区信息失败，{e},你可以检查你的网路或者代理。", style="bold red")
            return scene_list
        res_shop = BeautifulSoup(res.text, "lxml")
        city_scene = res_shop.find_all("a", attrs={"class": "guide-main-item"})
        for item in city_scene:
            try:
                city_scene_name = item.find("p", attrs={"class": "title"})
                if city_scene_name is None:
                    continue
                city_scene_name = city_scene_name.string
                city_scene_url = item["href"]
                scene_list.append({
                    "name": city_scene_name,
                    "url": city_scene_url
                })
            except TypeError:
                self.console.print(f"[red]获取景区信息失败[/red]")
            except Exception as e:
                self.console.print(f"[red]获取景区信息失败：{e},你的ip可能被封禁了！[/red]")
        if len(scene_list) == 0:
            self.console.print(
                f"[yellow]获取{city_name}相关景区的信息[red]失败[/red]:[blue]{[item['name'] for item in scene_list]}[/blue]",
                style="bold")
            return scene_list
        self.console.print(
            f"[yellow]获取{city_name}相关景区的信息[green]成功[/green]:[blue]{[item['name'] for item in scene_list]}[/blue]",
            style="bold")
        return scene_list

    def get_city_scene_info(self, city_scene_name, city_scene_url: str, province: str, city: str) -> None:
        """
        获取景区的id
        :param city:城市
        :param province: 省份
        :param city_scene_name: 景点的名称
        :param city_scene_url: 景点对应在携程的主页yrl
        :return:
        """
        pattern_businessId = r'/(\d+)\.html$'
        match = re.search(pattern_businessId, city_scene_url)
        businessId = ""
        districtId = ""
        if match:
            businessId = match.group(1)

        pattern_districtId = r'(\d+)/'
        match = re.search(pattern_districtId, city_scene_url)
        if match:
            districtId = match.group(1)
        _params = self.generate_scene_comments_params()
        _data = {
            "businessId": str(businessId),
            "districtId": int(districtId),
            "head": {
                "auth": "",
                "cid": _params["_fxpcqlniredt"],
                "ctok": "",
                "cver": "1.0",
                "extension": [],
                "lang": "01",
                "sid": "8888",
                "syscode": "09",
                "xsid": ""
            },
            "scene": "basic",
            "useSightExtend": True
        }
        _params = self.generate_scene_comments_params()
        try:
            _res = requests.post(
                url=GET_SCENE_INFO,
                params=_params,
                headers={
                    "User-Agent": get_fake_user_agent("mobile", False),

                },
                data=json.dumps(_data),
                proxies=my_get_proxy(),
                timeout=TIME_OUT

            )
            result = _res.json()
            try:
                scene_info = {
                    "name": city_scene_name,
                    "url": city_scene_url,
                    "resourceId": businessId,
                    "comment_total": result["commentCount"],
                    "comment_score": result["commentScore"],
                    "heat_score": result["heatScore"],
                    "tag_name": result.get("tagName", ""),
                    "poi_Level": result.get("poiLevel", ""),
                    "is_free": result["isFree"],
                }
                self.scene_list.append(scene_info)
                try:
                    script_path = os.path.abspath(__file__)
                    grandparent_dir = os.path.dirname(os.path.dirname(script_path))
                    path_file = os.path.join(grandparent_dir, f"data\{province}\{city}\{city_scene_name}")
                    os.makedirs(path_file, exist_ok=True)
                    dateToJsonFileSceneInfo(scene_info, path_file)
                except Exception as e:
                    self.console.print(f"[red]保存景点{city_scene_name}信息失败：{e}。[/red]")

            except Exception as e:
                self.console.print(f"[red]解析景点{city_scene_name}信息失败：{e}。[/red]")
        except Exception as e:
            self.console.print(f"[red]获取景点{city_scene_name}信息失败：{e},你可以检查你的网路或者代理。[/red]")

    def get_all_scene_info(self, city_list: list, province: str, city_name: str) -> None:
        """
        获取所有景区的信息
        :param city_name: 城市名称
        :param province: 省份名称
        :param city_list: 城市景区列表
        :return:
        """
        for city in city_list:
            self.get_city_scene_info(city["name"], city["url"], province, city_name)

    def get_scene_comments(self, resourceId: int, page_index: int, page_size) -> list:
        _params = self.generate_scene_comments_params()
        _data = {
            "arg": {
                "channelType": 7,
                "collapseType": 1,
                "commentTagId": 0,
                "pageIndex": page_index,
                "pageSize": page_size,
                "resourceId": int(resourceId),
                "resourceType": 11,
                "sortType": 3,
                "sourceType": 1,
                "starType": 0,
                "videoImageSize": "700_392",
            },
            "contentType": "json",
            "head": {
                "auth": "",
                "cid": _params["_fxpcqlniredt"],
                "ctok": "",
                "cver": "1.0",
                "lang": "01",
                "sid": "8888",
                "extension": [{
                    "name": "tecode",
                    "value": "h5"
                }],
                "syscode": "09",
                "xsid": "",
            }
        }
        try:
            res = self.sees.post(
                url=GET_COMMENT,
                params=_params,
                # 不能直接使用_data，要用json.dumps()转换成json格式
                data=json.dumps(_data),
                headers={
                    "User-Agent": get_fake_user_agent("mobile"),
                    # "Cookie": self.sees.cookies.get_dict(),
                },
                proxies=my_get_proxy(),
                timeout=TIME_OUT
            )
        except Exception as e:
            self.console.print(f"[red]获取景点评论第{page_index}页失败,你可以检查你的网路或者代理[/red]")
            return []
        return res.json()

    def generate_scene_comments_params(self) -> dict:
        """
        生成请求景区评论的 params参数
        :return:
        """
        random_number = random.randint(100000, 999999)
        return {
            "_fxpcqlniredt": self.sees.cookies.get("GUID"),
            "x-traceID": self.sees.cookies.get("GUID") + "-" + str(int(time.time() * 1000000)) + "-" + str(
                random_number)
        }

    @staticmethod
    def get_province() -> list:
        script_path = os.path.abspath(__file__)
        grandparent_dir = os.path.dirname(os.path.dirname(script_path))
        path = os.path.join(grandparent_dir, "city.json")
        cities_json = jsonFileToDate(path)
        cities_json = cities_json["city"]

        return cities_json

    @staticmethod
    def generate_city_file() -> None:
        create_file()

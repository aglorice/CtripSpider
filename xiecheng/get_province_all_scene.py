# -*- coding = utf-8 -*-
# @Time :2023/7/14 12:59
# @Author :小岳
# @Email  :401208941@qq.com
# @PROJECT_NAME :scenic_spots_comment
# @File :  get_province_all_scene.py
import time

from config import CITY_SLEEP_TIME, SCENE_SLEEP_TIME, IS_OVER
from utils.generate_excel import generate_excel
from utils.utils import get_is_exist
from xiecheng.get_comments_pool import get_comments_pool
from xiecheng.xiecheng_api import XieCheng
from rich.console import Console


def get_province_all_scene(xc: XieCheng, console: Console) -> None:
    city_list = XieCheng.get_province()
    for city in city_list:
        province_name = city["name"]
        console.rule(f"[blue]正在爬取{province_name}的所有热门地区的热门景点的数据", style="bold yellow", characters="=", )
        for item in city["city"]:
            city_list = xc.get_city_scene(item["name"], item["url"])
            xc.get_all_scene_info(city_list, province_name, item["name"])

            # 爬取景区的评论
            for _item in range(len(xc.scene_list)):
                # 先检测是否已经有景区的评论数据的excel表格，如果有则跳过
                if not IS_OVER and get_is_exist(xc.scene_list[_item]["name"], item["name"], province_name):
                    console.print(f"[yellow]已经爬取过{xc.scene_list[_item]['name']}的评论数据,[/yellow]", style="bold")
                    continue
                comment = get_comments_pool(xc, console, _item)
                if len(comment) == 0:
                    continue
                generate_excel(province_name, item["name"], xc.scene_list[_item]["name"], comment, console)
            time.sleep(SCENE_SLEEP_TIME)
            xc.scene_list = []
        console.print(f"[blue]爬取{province_name}的所有热门地区的热门景点的数据完成[/blue]", style="bold yellow")
        time.sleep(CITY_SLEEP_TIME)

# -*- coding = utf-8 -*-
# @Time :2023/7/13 14:50
# @Author :小岳
# @Email  :401208941@qq.com
# @PROJECT_NAME :scenic_spots_comment
# @File :  get_comments_pool.py
from rich.console import Console

from config import PAGESIZE, POOL_NUMBER, MAX_PAGE
from xiecheng.xiecheng_api import XieCheng
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_comments_pool(xc: XieCheng, console: Console, _index: int) -> list:
    """
    使用线程池获取景区评论数据
    :param xc: XieCheng类的实例
    :param console: 控制台输出
    :param _index: 景区列表的索引
    :return: 评论数据列表
    """
    comments_list = []
    threadPool = ThreadPoolExecutor(max_workers=POOL_NUMBER)
    thread_list = []

    # 当评论数大于3000条时限制爬取评论的页数
    try:
        if xc.scene_list[_index]["comment_total"] > MAX_PAGE:
            comment_total = MAX_PAGE
        else:
            comment_total = xc.scene_list[_index]["comment_total"]
    except Exception as e:
        console.print(f"获取景区评论数据返回数据异常，{e}", style="bold red")
        comment_total = 0
    console.print(f"正在爬取[yellow]{xc.scene_list[_index]['name']}[/yellow]的评论数据，预计爬取{comment_total}页的数据", style="bold green")
    try:
        for index in range(1, comment_total):
            thread = threadPool.submit(xc.get_scene_comments, xc.scene_list[_index]["resourceId"], index, PAGESIZE)
            thread_list.append(thread)

        for mission in as_completed(thread_list):
            try:
                result = mission.result()
                if result["result"]["items"]:
                    comments_list.extend(result["result"]["items"])
            except TypeError as e:
                console.print(f"获取评论的接口返回数据异常，{e},{result}，", style="bold red")
    except Exception as e:
        console.print(f"线程池出现问题，{e}", style="bold red")
    if not comments_list:
        console.print(f"[red]爬取[yellow]{xc.scene_list[_index]['name']}[/yellow]景区评论失败[/red]", style="bold green")
        return  []
    return comments_list

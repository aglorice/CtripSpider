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
    should_stop = False

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

    # 使用字典来跟踪任务和页码的对应关系
    future_to_page = {}
    try:
        for index in range(1, comment_total):
            future = threadPool.submit(xc.get_scene_comments, xc.scene_list[_index]["resourceId"], index, PAGESIZE)
            future_to_page[future] = index

        for future in as_completed(future_to_page):
            if should_stop:
                # 已经遇到空数据，跳过剩余任务的结果处理
                continue
            page_num = future_to_page[future]
            try:
                result = future.result()
                if result and result.get("result", {}).get("items"):
                    comments_list.extend(result["result"]["items"])
                elif result:
                    # 返回成功但items为空，说明已经没有更多数据了
                    console.print(f"[yellow]第{page_num}页返回数据为空，停止爬取后续页面[/yellow]")
                    should_stop = True
            except TypeError as e:
                console.print(f"[red]第{page_num}页返回数据格式异常: {e}[/red]", style="bold red")
            except Exception as e:
                console.print(f"[red]第{page_num}页处理异常: {e}[/red]", style="bold red")
    except Exception as e:
        console.print(f"线程池出现问题，{e}", style="bold red")
    finally:
        threadPool.shutdown(wait=False)

    if not comments_list:
        console.print(f"[red]爬取[yellow]{xc.scene_list[_index]['name']}[/yellow]景区评论失败[/red]", style="bold green")
        return []
    console.print(f"[green]共爬取{len(comments_list)}条评论数据[/green]")
    return comments_list

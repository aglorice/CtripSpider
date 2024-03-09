# -*- coding = utf-8 -*-
# @Time :2023/7/9 20:53
# @Author :小岳
# @Email  :401208941@qq.com
# @PROJECT_NAME :scenic_spots_comment
# @File :  utils.py
import json
import os


def dateToJsonFile(city: list) -> None:
    """
    将答案写入文件保存为json格式
    :param city:
    :return:
    """
    to_dict = {
        "city": city,
    }
    # json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False
    json_data = json.dumps(to_dict, ensure_ascii=False)
    script_path = os.path.abspath(__file__)
    grandparent_dir = os.path.dirname(os.path.dirname(script_path))
    path = os.path.join(grandparent_dir, "city.json")
    with open(path, 'w', encoding="utf-8") as f_:
        f_.write(json_data)


def dateToJsonFileSceneInfo(scene_info: dict, path: str) -> None:
    """
    将答案写入文件保存为json格式
    :param path:
    :param scene_info: 景区信息
    :return:
    """
    # json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False
    json_data = json.dumps(scene_info, ensure_ascii=False)
    path = os.path.join(path, "scene_info.json")
    with open(path, 'w', encoding="utf-8") as f_:
        f_.write(json_data)


def jsonFileToDate(file: str) -> dict:
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def create_directories(data: dict, parent_path='') -> None:
    for item in data["city"]:
        name = item['name']
        _path = os.path.join(parent_path, name)
        os.makedirs(_path, exist_ok=True)
        for _item in item["city"]:
            path = os.path.join(_path, _item["name"])
            os.makedirs(path, exist_ok=True)


def create_file() -> None:
    script_path = os.path.abspath(__file__)
    grandparent_dir = os.path.dirname(os.path.dirname(script_path))
    create_directories(jsonFileToDate("city.json"), grandparent_dir + "\\data")


def get_is_exist(scene_name: str, city_name: str, province: str) -> bool:
    script_path = os.path.abspath(__file__)
    grandparent_dir = os.path.dirname(os.path.dirname(script_path))

    path = os.path.join(grandparent_dir, "data", province, city_name,scene_name, f"{scene_name}.xlsx")
    return os.path.exists(path)

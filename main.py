import math
import random
from rich.console import Console

from config import AREAS
from utils.generate_excel import generate_excel
from xiecheng.get_comments_pool import get_comments_pool
from xiecheng.get_province_all_scene import get_province_all_scene
from xiecheng.xiecheng_api import XieCheng

# 设置控制台的宽度
console = Console(width=150)

if __name__ == '__main__':
    xc = XieCheng(console)
    get_province_all_scene(xc, console)

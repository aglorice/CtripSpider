from config import AREAS
from utils.utils import dateToJsonFile, create_file
from xiecheng.xiecheng_api import XieCheng
from rich.console import Console

if __name__ == '__main__':
    xc = XieCheng(console=Console())
    _city = xc.get_areas()
    city = [item for item in _city if item["name"] in AREAS]
    dateToJsonFile(city)
    xc.console.print(f"获取到{len(city)}个城市的数据,你可以根据自己的需要删减city.json中的城市，", style="bold green")

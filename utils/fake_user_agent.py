# -*- coding = utf-8 -*-
# @Time :2023/7/13 21:32
# @Author :小岳
# @Email  :401208941@qq.com
# @PROJECT_NAME :scenic_spots_comment
# @File :  fake_user_agent.py
from fake_useragent import UserAgent
import random
from config import IS_FAKE_USER_AGENT


def get_fake_user_agent(ua: str, default=True) -> str:
    match ua:
        case "mobile":
            if IS_FAKE_USER_AGENT and default:
                ua = get_mobile_user_agent()
                return ua
            else:
                return "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/114.0.0.0"
        case "pc":
            if IS_FAKE_USER_AGENT and default:
                ua = UserAgent()
                return ua.random
            else:
                return "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36 Edg/103.0.1264.49"


def get_mobile_user_agent() -> str:
    platforms = [
        'iPhone; CPU iPhone OS 14_6 like Mac OS X',
        'Linux; Android 11.0.0; Pixel 5 Build/RD1A.201105.003',
        'Linux; Android 8.0.0; Pixel 5 Build/RD1A.201105.003',
        'iPad; CPU OS 14_6 like Mac OS X',
        'iPad; CPU OS 15_6 like Mac OS X',
        'Linux; U; Android 9; en-us; SM-G960U Build/PPR1.180610.011',  # Samsung Galaxy S9
        'Linux; U; Android 10; en-us; SM-G975U Build/QP1A.190711.020',  # Samsung Galaxy S10
        'Linux; U; Android 11; en-us; SM-G998U Build/RP1A.200720.012',  # Samsung Galaxy S21 Ultra
        'Linux; U; Android 9; en-us; Mi A3 Build/PKQ1.180904.001',  # Xiaomi Mi A3
        'Linux; U; Android 10; en-us; Mi 10T Pro Build/QKQ1.200419.002',  # Xiaomi Mi 10T Pro
        'Linux; U; Android 11; en-us; LG-MG870 Build/RQ1A.210205.004',  # LG Velvet
        'Linux; U; Android 11; en-us; ASUS_I003D Build/RKQ1.200826.002',  # Asus ROG Phone 3
        'Linux; U; Android 10; en-us; CLT-L29 Build/10.0.1.161',  # Huawei P30 Pro
    ]

    browsers = [
        'Chrome',
        'Firefox',
        'Safari',
        'Opera',
        'Edge',
        'UCBrowser',
        'SamsungBrowser'
    ]

    platform = random.choice(platforms)
    browser = random.choice(browsers)

    match browser:
        case 'Chrome':
            version = random.randint(70, 90)
            return f'Mozilla/5.0 ({platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.#{random.randint(1000, 9999)}.#{random.randint(10, 99)} Mobile Safari/537.36'

        case 'Firefox':
            version = random.randint(60, 80)
            return f'Mozilla/5.0 ({platform}; rv:{version}.0) Gecko/20100101 Firefox/{version}.0'

        case 'Safari':
            version = random.randint(10, 14)
            return f'Mozilla/5.0 ({platform}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version}.0 Safari/605.1.15'

        case 'Opera':
            version = random.randint(60, 80)
            return f'Mozilla/5.0 ({platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.#{random.randint(1000, 9999)}.#{random.randint(10, 99)} Mobile Safari/537.36 OPR/{version}.0'

        case 'Edge':
            version = random.randint(80, 90)
            return f'Mozilla/5.0 ({platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.#{random.randint(1000, 9999)}.#{random.randint(10, 99)} Mobile Safari/537.36 Edg/{version}.0'

        case 'UCBrowser':
            version = random.randint(12, 15)
            return f'Mozilla/5.0 ({platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 UBrowser/{version}.1.2.49 Mobile Safari/537.36'

        case 'SamsungBrowser':
            version = random.randint(10, 14)
            return f'Mozilla/5.0 ({platform}) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/{version}.0 Chrome/63.0.3239.26 Mobile Safari/537.36'

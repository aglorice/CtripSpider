# 爬取指定身份内的所有地区景点的评论数据
areas = ['四川']

# 爬取评论时每页的数据
pageSize = 20

# 是否启动代理
is_proxy = False

# 是否启动随机UA
is_fake_user_agent = True

# 是否启动验证ssl
is_verify = False

# 是否要覆盖已经保存的excel文件
is_over = False

# 延时时间（城市）
CITY_SLEEP_TIME = 10

# 景区之间的休眠时间
SCENE_SLEEP_TIME = 10

# 线程池数量
POOL_NUMBER = 50

# 请求超时时间
TIME_OUT = 5

# 爬取评论的页数
MAX_PAGE = 300

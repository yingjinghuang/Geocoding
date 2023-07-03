# python 3.7
# author: Yingjing Huang
# Date: 2021/8/27
# 使用百度地图api进行地理编码

from convert_coords import * # 转换坐标系的代码
import requests
import time, random
import pandas as pd

aks = [
    "your_ak"
]
raw_file = "file.csv"
# address field
field = "地址"

def get_latlon(dd):
    ak = random.choice(aks)
    d = dd.strip()
    url = "http://api.map.baidu.com/geocoding/v3/"
    params = {
        "address": d,
        "output": "json",
        "ak": ak,
        "ret_coordtype": "gcj02ll"  # 返回gcj02ll坐标
    }
    try:
        res = requests.get(url, params=params)
        temp = res.json()
        loc = (temp["result"]["location"]["lng"], temp["result"]["location"]["lat"])
        return loc
    except Exception as e:
        print(e)
        print(res.content)
        time.sleep(5)
        return get_latlon(dd)

data = pd.read_csv(raw_file)

data["gcj02"] = data.apply(lambda x: get_latlon(x[field]), axis=1)
data["wgs84"] = data.apply(lambda x: gcj02_to_wgs84(x["gcj02"][0], x["gcj02"][1]), axis=1)
# 将经纬度分为两列
data["gcj02_lng"] = data["gcj02"].apply(lambda x: x[0])
data["gcj02_lat"] = data["gcj02"].apply(lambda x: x[1])
del data["gcj02"]
data["wgs84_lng"] = data["wgs84"].apply(lambda x: x[0])
data["wgs84_lat"] = data["wgs84"].apply(lambda x: x[1])
del data["wgs84"]

data.to_csv("out.csv")

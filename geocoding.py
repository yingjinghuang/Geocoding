# Author: ivy
# Version: Python 3.8
# Date: 2021/03/12

import requests
import time

ak = "your baidu ak"
address = "your address"

def get_latlon(address, ak):
    d = address.strip()
    url = "http://api.map.baidu.com/geocoding/v3/"
    params = {
        "address": d,
        "output": "json",
        "ak": ak,
        "ret_coordtype": "gcj02ll"  # 返回gcj02ll坐标，可以选择其他坐标系
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

if __name__ == "__main__":
    get_latlon(address, ak)
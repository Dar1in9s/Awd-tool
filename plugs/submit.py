import requests
from libs.Misc import Log, Config


def submit(flags):
    """
    提交flag，用于批量提交flag
    传入flag格式：{target : [flag1, flag2, ...]}
    """
    url = 'http://47.112.138.115:9999/'                             # 提交flag的url
    header = {'Authorization': 'bf37f8391ad3283627b7234f72972d43'}  # 提交flag需要的http头

    for target, flags in flags.items():
        Log.blue('[*] {}'.format(target), end=' ====> ')
        Log.blue(flags)
        for flag in flags:
            flag = {'flag': flag.strip()}
            try:
                req = requests.post(url, data=flag, headers=header, timeout=2, proxies=Config.proxy)
                Log.show(req.content.decode('utf-8').strip())
            except requests.Timeout:
                Log.red('timeout')

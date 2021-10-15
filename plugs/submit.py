import requests
from libs.Misc import Log, Config


def submit(flags):
    """
    批量提交flag
    传入flag格式：{target : [flag1, flag2, ...]}
    """
    url = 'http://10.1.8.10/event/1/awd/flag/?token=4826efa9d50c137b&flag=%s'# 提交flag的url
    # 提交flag需要的http头

    for target, flags in flags.items():
        Log.blue('[*] {}'.format(target), end=' ====> ')
        Log.blue(flags)
        for flag in flags:
            flag = flag.strip()
            try:
                req = requests.post(url%flag, timeout=2, proxies=Config.proxy)
                Log.show(req.content.decode('utf-8').strip())
            except requests.Timeout:
                Log.red('timeout')

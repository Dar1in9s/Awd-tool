import requests
from libs.Misc import Log


def submit(flags):
    """
    提交flag，用于批量提交flag
    传入flag格式：{target : flag}
    """
    url = 'http://47.112.138.115:9999/'
    header = {'Authorization': 'bf37f8391ad3283627b7234f72972d43'}

    for target, flag in flags.items():
        Log.blue('[*] {}'.format(target), end=' ====> ')
        flag = {'flag': flag.strip()}
        try:
            req = requests.post(url, data=flag, headers=header, timeout=2)
            Log.show(req.content.decode('utf-8').strip())
        except requests.Timeout:
            Log.red('timeout')

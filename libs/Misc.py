import json


def list_rm_repeat(origin_list):
    """列表去重"""
    _list = []
    for i in origin_list:
        if i not in _list:
            _list.append(i)
    return _list


class Log:
    @staticmethod
    def success(info):
        print("\033[32mSUCCESS: {}\033[0m".format(info))

    @staticmethod
    def error(info):
        print("\033[31mERROR: {}\033[0m".format(info))

    @staticmethod
    def eg(info):
        print("\033[33mE.g: {}\033[0m".format(info))

    @staticmethod
    def help(cmd, description):
        print('  \033[36m{}'.format(cmd).ljust(25, ' '), '\033[0m{}'.format(description))

    @staticmethod
    def show(info, end="\n"):
        print(info, end=end)

    @staticmethod
    def red(info, end="\n"):
        print("\033[31m{}\033[0m".format(info), end=end)

    @staticmethod
    def green(info, end="\n"):
        print("\033[32m{}\033[0m".format(info), end=end)

    @staticmethod
    def blue(info, end="\n"):
        print("\033[36m{}\033[0m".format(info), end=end)


class Config:
    """配置属性"""
    proxy = {}
    flag_format = None
    eval_base64_coding = True
    undead_horse_name = None
    custom_request_headers = {}

    @staticmethod
    def update_config():
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                json_data = ''
                for line in f.readlines():
                    if line.strip() and '//' != line.strip()[:2]:
                        json_data += line
                data = json.loads(json_data)

            Config.undead_horse_name = data['undead_horse_name']
            Config.proxy = data['proxy']
            Config.flag_format = r'{}'.format(data['flag_format']) if data['flag_format'] else None
            Config.eval_base64_coding = data['eval_base64_coding']
            Config.custom_request_headers = data['custom_request_headers']
        except Exception as e:
            Log.error('Update config error. {}'.format(e))

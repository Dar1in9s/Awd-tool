#! -*- coding:utf-8 -*-
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from libs.Awd import Awd
from libs.Misc import Config
import os


def main():
    os.system(" ")
    history = InMemoryHistory()
    command = WordCompleter([
        'help', 'clear_targets', 'add_target', 'show_targets',
        'del_webshell', 'add_webshell', 'show_webshell',
        'do_cache', 'load_cache', 'clear_cache',
        'show_flag', 'operate_shell', 'upload_horse', 'submit_flag', 'custom_attack',
        'exit', 'quit'
    ])
    awd = Awd()
    while True:
        user_input = prompt('$ ', history=history, completer=command)
        user_input = user_input.strip()
        Config.update_config()
        if user_input == 'exit' or user_input == 'quit':
            break
        elif user_input == 'help':
            awd.help()
        elif user_input == 'clear_targets':
            awd.Targets.clear()
        elif user_input == 'add_target':
            awd.Targets.add()
        elif user_input == 'show_targets':
            awd.Targets.show()
        elif user_input == 'do_cache':
            awd.Cache.do_cache(awd.Targets, awd.WebShell)
        elif user_input == 'load_cache':
            awd.Cache.load_cache(awd.Targets, awd.WebShell)
        elif user_input == 'clear_cache':
            awd.Cache.clear_cache()
        elif user_input == 'add_webshell':
            awd.WebShell.add()
        elif user_input == 'show_webshell':
            awd.WebShell.show()
        elif user_input == 'del_webshell':
            awd.del_webshell()
        elif user_input == 'show_flag':
            awd.show_flag()
        elif user_input == 'operate_shell':
            awd.operate_shell()
        elif user_input == 'upload_horse':
            awd.operate_shell(True)
        elif user_input == 'submit_flag':
            awd.submit_flag()
        elif user_input == 'custom_attack':
            awd.custom_attack()
        else:
            print('\033[33mWhat Do You Mean?\033[0m')
        print()
    print('\033[36mBye~\033[0m')


if __name__ == '__main__':
    main()

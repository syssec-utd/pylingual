import os, sys
from renus.commands.help import Help

def run():
    arg = sys.argv
    os.system('cls')
    if len(arg) < 2:
        Help()
    if len(arg) == 2:
        getattr(__import__(f'renus.commands.{arg[1]}.run', fromlist=['']), 'run')()
    elif len(arg) > 2:
        getattr(__import__(f'renus.commands.{arg[1]}.run', fromlist=['']), 'run')(arg[2:])
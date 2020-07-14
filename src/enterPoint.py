from windows import run as windowsrun
from consolev import main as consolemain
import bilibili as b
import os
import sys
if __name__ == '__main__':
    argv=sys.argv
    if argv[1]=="--windows":
        windowsrun()
    elif argv[1]=="--console":
        consolemain()
    elif argv[1]=="--download":
        os.system("you-get --format==%s %s" %(b.Var.setting.format,b.Bilibili(b.Var.setting,argv[2]).link))
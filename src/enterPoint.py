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
        try:
            os.system("you-get --format==flv %s" %b.Bilibili(b.Var.setting,argv[2]).link)
        except:
            os.system("you-get --format==flv480 %s" %b.Bilibili(b.Var.setting,argv[2]).link)
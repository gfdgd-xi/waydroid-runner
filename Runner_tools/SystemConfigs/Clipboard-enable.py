#A Python3 Program
#DO NOT RUNNING BY SUDO!
import os
import sys

def Running_err():                            #遇到异常通用退出函数
    print('-程序运行出现异常,即将退出')
    sys.exit(1)

print('-请在下方输入您当前的sudo用户密码')                 #拿到sudo权限
os.system('sudo echo 提权完成! && clear')

print('-正在开启全局剪切板功能')
if os.system('lsb_release -a')!=0:              #检查是否能获取系统版本
    print('-警告:您的系统没有lsb_release指令,请安装它!')
    Running_err()

sys_name=os.popen('lsb_release -a').read()       #获取并判断系统版本,删掉不支持的
if sys_name.find('deepin')!=-1 and sys_name.find('apricot')!=-1:
    print('-不支持Deepin-v20!');Running_err()
if sys_name.find('UOS')!=-1:
    print('-不支持统信UOS!');Running_err()

print('-正在安装wl-clipboard')        #先安装wl-clipboard
if os.system('sudo apt update && sudo apt install wl-clipboard -y')!=0:
    print('-您的系统没有wl-clipboard包,无法开启剪切板同步功能!')
    Running_err()

print('-正在添加pyclip(pip3包)')
if sys_name.find('Ubuntu')!=-1 and (sys_name.find('kinetic')!=-1 or sys_name.find('mantic')!=-1):    #Ubuntu 23.04和23.10要特殊处理
    print('-检测到Ubuntu 23.04+,正在执行强制安装')
    os.system('python3 -m pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple  --break-system-packages')
else:
    os.system('python3 -m pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple')

print('\n-添加成功,程序运行完成!重启电脑后剪切板互通功能生效!')
sys.exit(0)

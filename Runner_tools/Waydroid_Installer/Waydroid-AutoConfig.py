#!/bin/python3
#Please DO NOT RUNNING BY sudo!
import os
import sys
os.chdir(os.path.split(os.path.realpath(__file__))[0]  #定位到当前运行目录

print('-请在下方输入您的sudo用户密码:')
os.system('sudo echo 提权完成! && clear')
print('本程序将默认开启以下功能:')
print('-建议使用Ubuntu')
print('1.开启多窗口模式')
print('2.默认防止屏幕旋转')
print('3.设置语言为中文/简体')
print('4.Deepin-v23下显示Wayland的安卓窗口光标')
print('5.开启剪切板互通功能\n')

a=input('-是否需要安装Magisk-Delta?是请输入y回车,不需要请直接回车:')      ##Magisk-Delta安装
if a=='y' or a=='Y':        
    print('-正在安装Magisk-Delta:',end="")
    if os.system('cd ../Magisk_Installer && python3 Magisk.py') == '0':
        print('成功!')
    else:print('失败!请自行查找原因!')
else:print('-已跳过Magisk-Delta安装,如果您以后需要可以在Waydroid运行器里安装')

os_release=os.popen('lsb_release -a').read()   ##检测系统版本,异常给os_release变量返回-1
if os.system('lsb_release -a && clear')!=0:
    print('运行异常,程序无法读取操作系统版本,请自行安装lsb_release应用!')
    os_release = -1

#以下程序先执行不需要启动session的部分,然后再启动需要启动session的部分
print('-正在设置语言为中文/简体') 


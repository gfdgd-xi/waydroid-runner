#A Python3 Program
#Please running by sudo!
import os
import sys

print('-开启全局剪切板功能')
print('-正在安装wl-clipboard')
if os.system('sudo apt install wl-clipboard')!=0:
    print('-您的系统没有wl-clipboard包,无法开启剪切板同步功能!')
    sys.exit(1)
print('-正在添加pyclip(pip3包)')
os.system('python3 -m pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple')
print('-添加成功,程序运行完成!')

#!/bin/env python3
# A Python3 Program
# You don't running by sudo
import os
import sys
f=open('/var/lib/waydroid/waydroid.cfg','r')    # 读取waydroid.cfg
a=f.read()       # 读入waydroid.cfg至a变量
f.close()        # 关闭文件防止bug/内存泄漏
if a.find('persist.sys.timezone') !=-1 or a.find('persist.sys.language')!=-1 or a.find('persist.sys.country')!=-1: sys.exit(0)
else: sys.exit(1)

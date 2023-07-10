#此应用请以root身份运行!
#Please running by root!
import os
os.system('waydroid container stop')
f = open('/var/lib/waydroid/waydroid.cfg','r+')
a=f.read()
if a.find('persist.sys.timezone')!=-1:
    print('警告:您已修改过语言!程序即将退出!')
f.close()

#-----------Main----------#
f = open('/var/lib/waydroid/waydroid.cfg','a+')
f.write('\npersist.sys.timezone=Asia/Shanghai\npersist.sys.language=zh\npersist.sys.country=CN')
f.close()
print('修改成功,正在应用更改:',end='')
if os.system('waydroid upgrade -o')!=0:print('失败!')
else:print('成功!')

os.system('systemctl restart waydroid-container.service')

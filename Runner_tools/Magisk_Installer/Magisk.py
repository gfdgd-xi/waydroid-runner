import os
os.chdir(os.path.split(os.path.realpath(__file__))[0]) # 定位到 data.img 所在目录以便脚本能正常调用
waydroid_path = '/var/lib/waydroid'
print('请在下方输入您的sudo用户密码:')
os.system('sudo echo 123 && clear')
if os.path.exists('datamount') == False:
    os.system('sudo mkdir datamount')
if os.path.exists('data.img') == False:
    print('关键文件缺失!请重新安装运行器!')
    exit(0)
os.system('sudo mount data.img')
os.system(f'cd {waydroid_path}/overlay && sudo mkdir -p system/etc/init')
os.system(f'cd datamount/system/etc/init && sudo cp -rf * {waydroid_path}/overlay/system/etc/init')
print('安装完成!')
print('正在清理目录:',end='')
os.system('sudo umount data.img && sudo rm -rf datamount')
print('完成')
print('\n程序运行结束!')

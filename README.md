<p width=100px align="center"><img src="runner.svg"></p>  
<h1 align="center">Waydroid 运行器 1.2.0.1</h1>  
<hr>  
<a href='https://gitee.com/gfdgd-xi/waydroid-runner/stargazers'><img src='https://gitee.com/gfdgd-xi/waydroid-runner/badge/star.svg?theme=dark' alt='star'></img></a>
<a href='https://gitee.com/gfdgd-xi/waydroid-runner/members'><img src='https://gitee.com/gfdgd-xi/waydroid-runner/badge/fork.svg?theme=dark' alt='fork'></img></a>  

## 介绍
Waydroid运行器是可以通过GUI形式半自动配置Waydroid的工具，使用户使用Waydroid更为方便。Waydroid本身存在很多因AOSP未考虑PC用户而产生的问题(如没有自带Houdini,默认英语,默认非小窗模式)而使用户使用起来非常难受,本运行器支持以GUI形式自动化安装以及配置Waydroid，并会创建快捷控制的快捷方式，可以用于玩游戏/刷视频/Android开发等。  

若您对本项目有疑问/需要一些帮助，可以进Q群:860232259，我们会尽其所能帮助(偶尔吹水也可以)  

## 配置要求
仅限启用 Wayland 的 x86-64 的 Linux，ARM64的在安装Magisk时可能需要重新制作data.img(教程有时间放出来) 显卡仅限Intel & AMD(独立显卡需要启动桌面环境时使用独立显卡,否则无法使用),只有英伟达显卡(连Intel核心显卡都没有的)当前无法使用本项目，建议使用xDroid/UEngine作为替代。 
 
**支持的系统（效果很好）**:Ubuntu 20.04 或更高、Deepin v23 Wayland(最新内测版最好)、Debian 11+(且安装了支持Wayland协议的桌面环境)、Linux MINT(KDE环境)    
**支持但效果不好**：YOYO OS以及上述系统的 X11 环境    
**支持但效果不好/很差，需要额外调教**：Deepin20.9、UOS家庭版、LingmoOS,Linux Mint(Cinnamon环境)……  
**不支持的系统**：UOS 专业版、UOS 教育版、UOS 学生版  

支持很好的桌面环境：DDE(deepin v23最新内测),GNOME 42及以上,KDE Plasma 5.27.4及以上(如果低于5.27,使用Wayland的bug估计不少),UnityX 7.7,Xfce 4.20  
支持很差的桌面环境：DDE20(deepin 20.9及以下,包括UOS家庭版，但不包括专业版、教育版、学生版),CutefishDE及其二改桌面环境,Budgie(等新版本支持Wayland)  
（更多系统测试中）  
  
***Deepin20/UOS 建议用 UEngine，虽然这个老掉牙了***  
***Waydroid 和 UEngine、Anbox 无法共存，可以输入以下命令卸载 UEngine***  
```bash
sudo apt purge uengine
sudo apt autopurge
```

## 在 deepin 23 上安装缺失依赖？
依赖下载地址：https://gfdgdxi.lanzoui.com/b01rwfgtg 密码:648f  

## 安装&使用教程
下载安装本软件,然后按照提示执行或使用功能即可  
如果 `waydroid-android-image-gapps` 这个包下载慢，可以到这里手动下载 deb 包：https://sourceforge.net/projects/waydroid-runner-apt-mirror/files/  

### LingmoOS 如何调教以便能运行 Waydroid？
***此方法有危险性，可能导致系统崩溃***  
安装源里其他的内核或者安装以下链接的内核并重启切换后用 Waydroid 运行器自带的 Waydroid 安装程序安装即可  
内核链接：https://gfdgdxi.lanzoue.com/b01r54ple    密码:35j0

### Deepin20/UOS 家庭版如何调教以便能运行 Waydroid？
***此方法有危险性，可能导致系统崩溃***  
目前 Waydroid 运行器自带的 Waydroid 安装程序（国内源）可以自动处理，但你依旧可以手动处理：  
### 升级系统 lxc 版本
在这里下载 lxc 包并升级：  
https://gfdgdxi.lanzoue.com/b01r5slyh  
密码:1zre
### 安装 Waydroid
使用运行器自带的安装程序即可，但如果要安装原版的 Waydroid，则需要自行编译 `python-gbinder`，方法如下：
```bash
sudo apt update
sudo apt install dpkg-dev git fakeroot
# 编译 libglibutil
git clone https://github.com/waydroid/libglibutil
cd libglibutil
sudo apt build-dep .
dpkg-buildpackage -b
cd ..
sudo apt install ./*.deb
# 编译 libgbinder
git clone https://github.com/waydroid/libgbinder
cd libgbinder
sudo apt build-dep .
dpkg-buildpackage -b
cd ..
sudo apt install ./*.deb
# 编译 python-gbinder
git clone https://github.com/waydroid/gbinder-python
cd gbinder-python
sudo apt build-dep .
sudo dpkg-buildpackage -b
cd ..
sudo apt install ./*.deb
```

## 当前系统的内核不支持运行 Waydroid 怎么办（如 Kail Linux）？
 **理论上不会出现此问题:Waydroid文档说明只要内核版本>=4.4即可** 
 **相反,很多时候跑不了Waydroid是因为LXC库太老/桌面太老或者跟Cinnamon一样不支持Wayland** 
可以自行寻找或编译支持的内核，或直接安装下面测试无问题的内核：  
https://gfdgdxi.lanzoue.com/b01r54ple    密码:35j0

## 安装 UEngine For Ubuntu 后无法正常启动 Waydroid 怎么办？
需要输入以下命令卸载 UEngine For Ubuntu（核心原因是 lxc 版本过老）  
```bash
sudo apt-mark unhold lxc lxc-templates liblxc1 liblxc-common lxc-utils
sudo apt purge uengine uengine-android-image uengine-modules-dkms
sudo apt update
sudo apt install lxc
```

## 效果演示
### Deepin20（X11）
需要使用 Sway/Weston 以及升级 lxc（运行器可以自动配置）  
![截图_选择区域_20230818174455.png](https://storage.deepin.org/thread/202308181800238151_截图_选择区域_20230818174455.png)
### UOS 家庭版
需要使用 Sway/Weston 以及升级 lxc（运行器可以自动配置）  
![截图_选择区域_20230818170557.png](https://storage.deepin.org/thread/202308181800235265_截图_选择区域_20230818170557.png)
### Deepin23
#### X11
需要使用 Sway/Weston（运行器可以自动配置）  
![截图_mainwindow.py_20230819164458.png](https://storage.deepin.org/thread/202308191649515402_截图_mainwindow.py_20230819164458.png)  
#### Wayland
无需特殊操作  
![截图_选择区域_20230817184441.png](https://storage.deepin.org/thread/20230818135604574_截图_选择区域_20230817184441.png)  
### Kail Linux（X11）
需要使用 Sway/Weston（运行器可以自动配置）以及更换内核（需手动设置）  
![截图_VirtualBoxVM_20230818195519.png](https://storage.deepin.org/thread/202308181955385166_截图_VirtualBoxVM_20230818195519.png)
### YOYO OS（X11）
需要使用 Sway/Weston（运行器可以自动配置）  
![Screenshot_20230817_182953.png](https://storage.deepin.org/thread/202308181356082869_Screenshot_20230817_182953.png)  
### LingmoOS
需要使用 Sway/Weston（运行器可以自动配置）  
![VirtualBox_Windows_19_08_2023_13_07_44.png](https://storage.deepin.org/thread/202308191649503740_VirtualBox_Windows_19_08_2023_13_07_44.png)
### Ubuntu
#### 20.04
需要使用 Sway/Weston（运行器可以自动配置）  
![VirtualBox_Windows_18_08_2023_20_39_23.png](https://storage.deepin.org/thread/202308182040048408_VirtualBox_Windows_18_08_2023_20_39_23.png)
#### 22.04
无需特殊操作  
![截图 2023-08-19 16-39-14.png](https://storage.deepin.org/thread/202308191649502677_截图2023-08-1916-39-14.png)
### Openkylin
#### X11
需要使用 Sway/Weston（运行器可以自动配置）且需要升级系统 lxc 版本（需手动设置）  
![2023-08-19_16-12-21.png](https://storage.deepin.org/thread/202308191649508531_2023-08-19_16-12-21.png)
#### Wayland
需要升级系统 lxc 版本（需手动设置）  
![2023-08-19_16-12-21.png](https://storage.deepin.org/thread/202308191649508531_2023-08-19_16-12-21.png)
### UbuntuKylin
需要使用 Sway/Weston（运行器可以自动配置）  
![VirtualBox_Windows_18_08_2023_21_27_02.png](https://storage.deepin.org/thread/202308191653274330_VirtualBox_Windows_18_08_2023_21_27_02.png)



## 历史版本
### 1.2.0（2023年09月29日）
**※1、修复GPU切换无效问题**  
**※2、修复部分脚本识别Session运行状态失败的问题**  
**※3、增加剪切板与Linux主系统互通功能(仅限Wayland模式)**  
**※4、增加GMS注册需要的Android-id获取功能**  
**※5、(重磅更新)一键配置功能全面升级,窗口化/谷歌拼音输入法/防止旋转/剪切板互通等一次到位**  
**※6、修复Waydroid运行器全屏显示时主系统死机问题**  

![图片.png](https://storage.deepin.org/thread/202309291503561223_图片.png)



### 1.1.0（2023年08月19日）
**※1、支持在 Deepin20/UOS 安装 Waydroid（效果无法保证且需要升级系统组件，容易导致系统问题，且在 UOS 下要开启开发者模式）**  
**※2、修复在 Deepin 23 运行时因为缺少 PIL 库导致无法运行的问题**  
**※3、支持在 X11 下使用 Waydroid 并自动启动 Sway/Weston**  
**※4、修复 Waydroid 应用商店可能出现 Session Stop 的问题**   
**※5、支持切换 Waydroid GPU**  
**※6、新增右键打开 APK 功能**  
**※7、更换程序图标**  
**※8、新增关闭 Waydroid 多窗口功能**  
**※9、新增安装 Widevine 功能**  
**※10、修复 Waydroid 运行器 1.0.0 在 X11 环境安装 Waydroid 后无法正常在 Weston/Sway 显示主界面**  
11、新增设置屏幕自动旋转的功能  
12、新增修复 Waydroid 多窗口在部分桌面环境无法显示鼠标问题的功能  


![VirtualBox_Windows_18_08_2023_21_27_02.png](https://storage.deepin.org/thread/202308191653274330_VirtualBox_Windows_18_08_2023_21_27_02.png)



![Screenshot_20230817_182953.png](https://storage.deepin.org/thread/202308181356082869_Screenshot_20230817_182953.png)  
![截图_选择区域_20230817184441.png](https://storage.deepin.org/thread/20230818135604574_截图_选择区域_20230817184441.png)  

![截图_选择区域_20230818170557.png](https://storage.deepin.org/thread/202308181800235265_截图_选择区域_20230818170557.png)

![截图_选择区域_20230818174455.png](https://storage.deepin.org/thread/202308181800238151_截图_选择区域_20230818174455.png)

![截图_VirtualBoxVM_20230818195519.png](https://storage.deepin.org/thread/202308181955385166_截图_VirtualBoxVM_20230818195519.png)

![VirtualBox_Windows_18_08_2023_20_39_23.png](https://storage.deepin.org/thread/202308182040048408_VirtualBox_Windows_18_08_2023_20_39_23.png)

![截图_mainwindow.py_20230819164458.png](https://storage.deepin.org/thread/202308191649515402_截图_mainwindow.py_20230819164458.png)
![截图 2023-08-19 16-39-14.png](https://storage.deepin.org/thread/202308191649502677_截图2023-08-1916-39-14.png)
![2023-08-19_16-14-49.png](https://storage.deepin.org/thread/202308191649502332_2023-08-19_16-14-49.png)
![2023-08-19_16-12-21.png](https://storage.deepin.org/thread/202308191649508531_2023-08-19_16-12-21.png)
![VirtualBox_Windows_19_08_2023_13_07_44.png](https://storage.deepin.org/thread/202308191649503740_VirtualBox_Windows_19_08_2023_13_07_44.png)




### 1.0.0（2023年08月03日）
**※1、新增 Waydroid 主程序安装功能、镜像下载功能及其国内源**  
**※2、支持安装 Magisk、Libhoudini（二进制翻译器，可以运行 ARM APK）**  
**※3、支持对 Waydroid 的初步控制**  
**※4、支持安装/卸载 Android 应用**  
**※5、提供应用商店以安装 APK**  
![截图_20230803092541.png](https://storage.deepin.org/thread/202308030955174196_截图_20230803092541.png)  
![截图_20230803092511.png](https://storage.deepin.org/thread/202308030955175344_截图_20230803092511.png)  
![截图_20230803092449.png](https://storage.deepin.org/thread/202308030955172185_截图_20230803092449.png)  



## 源码安装教程
```bash
git clone https://gitee.com/gfdgd-xi/waydroid-runner
cd waydroid-runner 
make install -j4
```

## 参与贡献
@Telegram HuskyDG 巨佬贡献的 `Magisk` 安装到 `/system` 分区的方案和他的 `Magisk-Delta`  
@casualsuek 的 `Waydroid-Script` 代码    
@Quackdoc 的 Waydroid-Choose-gpu.sh  

# ©2023~Now gfdgd xi、Bail、LFRon

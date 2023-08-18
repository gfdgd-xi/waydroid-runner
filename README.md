<p width=100px align="center"><img src="runner.svg"></p>  
<h1 align="center">Waydroid 运行器 1.0.0.1</h1>  
<hr>  
<a href='https://gitee.com/gfdgd-xi/waydroid-runner/stargazers'><img src='https://gitee.com/gfdgd-xi/waydroid-runner/badge/star.svg?theme=dark' alt='star'></img></a>
<a href='https://gitee.com/gfdgd-xi/waydroid-runner/members'><img src='https://gitee.com/gfdgd-xi/waydroid-runner/badge/fork.svg?theme=dark' alt='fork'></img></a>  

## 介绍
Waydroid运行器是可以通过GUI形式半自动配置Waydroid的工具，使用户使用Waydroid更为方便。Waydroid本身存在很多因AOSP未考虑PC用户而产生的问题(如没有自带Houdini,默认英语,默认非小窗模式)而使用户使用起来非常难受,本运行器支持以GUI形式自动化安装以及配置Waydroid，并会创建快捷控制的快捷方式，可以用于玩游戏/刷视频/Android开发等。  

若您对本项目有疑问/需要一些帮助，可以进Q群:872491938，我们会尽其所能帮助(偶尔吹水也可以)  

## 配置要求
仅限启用 Wayland 的 x86-64 的 Linux，ARM64的在安装Magisk时可能需要重新制作data.img(教程有时间放出来) 显卡仅限Intel & AMD(独立显卡需要启动桌面环境时使用独立显卡,否则无法使用),只有英伟达显卡(连Intel核心显卡都没有的)当前无法使用本项目，建议使用xDroid/UEngine作为替代。 
 
支持的系统（效果很好）:Ubuntu 20.04 或更高、Deepin v23 Wayland(最新内测版最好)、Debian 11+(且安装了支持Wayland协议的桌面环境)、Linux MINT(KDE环境)  
支持但效果不好/很差，需要额外调教：Deepin20.9、UOS家庭版、UOS专业版（不支持 4.19 内核）、LingmoOS,Linux Mint(Cinnamon环境)……  

支持很好的桌面环境:DDE(deepin v23最新内测),GNOME 42及以上,KDE Plasma 5.27.4及以上(如果低于5.27,使用Wayland的bug估计不少),UnityX 7.7,Xfce 4.20  
支持很差的桌面环境:DDE(deepin 20.9及以下,包括UOS家庭版和专业版),CutefishDE及其二改桌面环境,Budgie(等新版本支持Wayland)  
（更多系统测试中）  
  
***Deepin20/UOS 建议用 UEngine，虽然这个老掉牙了***  
***目前尚未测试 Waydroid 是否与 UEngine、xDroid 冲突***  

## 安装&使用教程
下载安装本软件,然后按照提示执行或使用功能即可  

## 当前系统的内核不支持运行 Waydroid 怎么办？
 **理论上不会出现此问题:Waydroid文档说明只要内核版本>=4.4即可** 
 **相反,很多时候跑不了Waydroid是因为LXC库太老/桌面太老或者跟Cinnamon一样不支持Wayland** 
可以自行寻找或编译支持的内核，或直接安装下面测试无问题的内核：  
https://gfdgdxi.lanzoue.com/b01r54ple    密码:35j0

## 历史版本
### 1.1.0（2023年08月？？日）
？？？

![Screenshot_20230817_182953.png](https://storage.deepin.org/thread/202308181356082869_Screenshot_20230817_182953.png)  
![截图_选择区域_20230817184441.png](https://storage.deepin.org/thread/20230818135604574_截图_选择区域_20230817184441.png)  



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


## ©2023~Now gfdgd xi、Bail、LFRon
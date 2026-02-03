<p width=100px align="center"><img src="runner.svg"></p>  
<h1 align="center">Waydroid Runner 1.2.0.1</h1>  
<hr>  
<a href='https://gitee.com/gfdgd-xi/waydroid-runner/stargazers'><img src='https://gitee.com/gfdgd-xi/waydroid-runner/badge/star.svg?theme=dark' alt='star'></img></a>
<a href='https://gitee.com/gfdgd-xi/waydroid-runner/members'><img src='https://gitee.com/gfdgd-xi/waydroid-runner/badge/fork.svg?theme=dark' alt='fork'></img></a>  

## Introduction
Waydroid Runner is a tool that can semi-automatically configure Waydroid through a GUI interface, making it more convenient for users to use Waydroid. Waydroid itself has many issues caused by AOSP not considering PC users (such as no built-in Houdini, default English language, default non-windowed mode), which makes it very difficult for users to use. This runner supports automated installation and configuration of Waydroid in GUI form, and creates shortcuts for quick control. It can be used for gaming, watching videos, Android development, and more.

If you have questions about this project or need help, you can join QQ group: 872491938, and we will do our best to help.

## System Requirements
Limited to x86-64 Linux with Wayland enabled. For ARM64, you may need to recreate data.img when installing Magisk (tutorial will be released when available). Graphics cards are limited to Intel and AMD (dedicated graphics cards need to be used when starting the desktop environment, otherwise they cannot be used). If you only have an NVIDIA graphics card (without even an Intel integrated graphics card), you currently cannot use this project. It is recommended to use xDroid/UEngine as an alternative.
 
**Supported systems (works well)**: Ubuntu 20.04 or higher, Deepin v23 Wayland (latest beta version is best), Debian 11+ (with desktop environment supporting Wayland protocol installed), Linux MINT (KDE environment)    
**Supported but not working well**: YOYO OS and X11 environments of the above systems    
**Supported but not working well/poorly, requires additional configuration**: Deepin 20.9, UOS Home Edition, LingmoOS, Linux Mint (Cinnamon environment), etc.  
**Unsupported systems**: UOS Professional Edition, UOS Education Edition, UOS Student Edition  

Well-supported desktop environments: DDE (deepin v23 latest beta), GNOME 42 and above, KDE Plasma 5.27.4 and above (if lower than 5.27, there are probably many bugs when using Wayland), UnityX 7.7, Xfce 4.20  
Poorly supported desktop environments: DDE20 (deepin 20.9 and below, including UOS Home Edition, but not Professional, Education, or Student editions), CutefishDE and its derivative desktop environments, Budgie (waiting for new version to support Wayland)  
(More systems under testing)  
  
**For Deepin20/UOS, it is recommended to use UEngine, although it is outdated**  
**Waydroid and UEngine, Anbox cannot coexist. You can enter the following command to uninstall UEngine**  
```bash
sudo apt purge uengine
sudo apt autopurge
```

## Installing Missing Dependencies on deepin 23?
Dependency download address: https://gfdgdxi.lanzoui.com/b01rwfgtg Password: 648f  

## Installation and Usage Tutorial
Download and install this software, then follow the prompts to execute or use the functions.  
If the `waydroid-android-image-gapps` package downloads slowly, you can manually download the deb package here: https://sourceforge.net/projects/waydroid-runner-apt-mirror/files/  

### How to Configure LingmoOS to Run Waydroid?
**This method is risky and may cause system crashes**  
Install other kernels from the repository or install the kernel from the following link and restart to switch, then use the Waydroid installer that comes with Waydroid Runner to install.  
Kernel link: https://gfdgdxi.lanzoue.com/b01r54ple    Password: 35j0

### How to Configure Deepin20/UOS Home Edition to Run Waydroid?
**This method is risky and may cause system crashes**  
Currently, the Waydroid installer that comes with Waydroid Runner (domestic source) can handle this automatically, but you can still handle it manually:  
### Upgrade System lxc Version
Download the lxc package here and upgrade:  
https://gfdgdxi.lanzoue.com/b01r5slyh  
Password: 1zre
### Install Waydroid
Use the installer that comes with the runner. However, if you want to install the original version of Waydroid, you need to compile `python-gbinder` yourself, as follows:
```bash
sudo apt update
sudo apt install dpkg-dev git fakeroot
# Compile libglibutil
git clone https://github.com/waydroid/libglibutil
cd libglibutil
sudo apt build-dep .
dpkg-buildpackage -b
cd ..
sudo apt install ./*.deb
# Compile libgbinder
git clone https://github.com/waydroid/libgbinder
cd libgbinder
sudo apt build-dep .
dpkg-buildpackage -b
cd ..
sudo apt install ./*.deb
# Compile python-gbinder
git clone https://github.com/waydroid/gbinder-python
cd gbinder-python
sudo apt build-dep .
sudo dpkg-buildpackage -b
cd ..
sudo apt install ./*.deb
```

## What if the Current System Kernel Does Not Support Running Waydroid (such as Kali Linux)?
 **Theoretically this problem should not occur: Waydroid documentation states that kernel version >= 4.4 is sufficient** 
 **On the contrary, many times Waydroid cannot run because the LXC library is too old/the desktop is too old or does not support Wayland like Cinnamon** 
You can find or compile a supported kernel yourself, or directly install the kernel tested below without problems:  
https://gfdgdxi.lanzoue.com/b01r54ple    Password: 35j0

## What to Do if Waydroid Cannot Start Normally After Installing UEngine For Ubuntu?
You need to enter the following command to uninstall UEngine For Ubuntu (the core reason is that the lxc version is too old)  
```bash
sudo apt-mark unhold lxc lxc-templates liblxc1 liblxc-common lxc-utils
sudo apt purge uengine uengine-android-image uengine-modules-dkms
sudo apt update
sudo apt install lxc
```

## Demo Screenshots
### Deepin20 (X11)
Requires using Sway/Weston and upgrading lxc (the runner can configure automatically)  
![Screenshot](https://storage.deepin.org/thread/202308181800238151_截图_选择区域_20230818174455.png)
### UOS Home Edition
Requires using Sway/Weston and upgrading lxc (the runner can configure automatically)  
![Screenshot](https://storage.deepin.org/thread/202308181800235265_截图_选择区域_20230818170557.png)
### Deepin23
#### X11
Requires using Sway/Weston (the runner can configure automatically)  
![Screenshot](https://storage.deepin.org/thread/202308191649515402_截图_mainwindow.py_20230819164458.png)  
#### Wayland
No special operations required  
![Screenshot](https://storage.deepin.org/thread/20230818135604574_截图_选择区域_20230817184441.png)  
### Kali Linux (X11)
Requires using Sway/Weston (the runner can configure automatically) and changing the kernel (manual setup required)  
![Screenshot](https://storage.deepin.org/thread/202308181955385166_截图_VirtualBoxVM_20230818195519.png)
### YOYO OS (X11)
Requires using Sway/Weston (the runner can configure automatically)  
![Screenshot](https://storage.deepin.org/thread/202308181356082869_Screenshot_20230817_182953.png)  
### LingmoOS
Requires using Sway/Weston (the runner can configure automatically)  
![Screenshot](https://storage.deepin.org/thread/202308191649503740_VirtualBox_Windows_19_08_2023_13_07_44.png)
### Ubuntu
#### 20.04
Requires using Sway/Weston (the runner can configure automatically)  
![Screenshot](https://storage.deepin.org/thread/202308182040048408_VirtualBox_Windows_18_08_2023_20_39_23.png)
#### 22.04
No special operations required  
![Screenshot](https://storage.deepin.org/thread/202308191649502677_截图2023-08-1916-39-14.png)
### Openkylin
#### X11
Requires using Sway/Weston (the runner can configure automatically) and upgrading system lxc version (manual setup required)  
![Screenshot](https://storage.deepin.org/thread/202308191649508531_2023-08-19_16-12-21.png)
#### Wayland
Requires upgrading system lxc version (manual setup required)  
![Screenshot](https://storage.deepin.org/thread/202308191649508531_2023-08-19_16-12-21.png)
### UbuntuKylin
Requires using Sway/Weston (the runner can configure automatically)  
![Screenshot](https://storage.deepin.org/thread/202308191653274330_VirtualBox_Windows_18_08_2023_21_27_02.png)

## Version History
### 1.2.0 (September 29, 2023)
**1. Fixed GPU switching issue**  
**2. Fixed script recognition failure for Session running status**  
**3. Added clipboard interoperability with Linux host system (Wayland mode only)**  
**4. Added Android-id retrieval function required for GMS registration**  
**5. (Major update) One-click configuration function fully upgraded, windowed mode/Google Pinyin input method/prevent rotation/clipboard interoperability all at once**  
**6. Fixed Waydroid Runner full-screen display causing host system freeze issue**  

### 1.1.0 (August 19, 2023)
**1. Support for installing Waydroid on Deepin20/UOS (effect cannot be guaranteed and requires upgrading system components, which may cause system issues, and requires enabling developer mode on UOS)**  
**2. Fixed issue where Deepin 23 could not run due to missing PIL library**  
**3. Support for using Waydroid on X11 and automatically starting Sway/Weston**  
**4. Fixed possible Session Stop issue in Waydroid app store**   
**5. Support for switching Waydroid GPU**  
**6. Added right-click to open APK function**  
**7. Changed program icon**  
**8. Added function to disable Waydroid multi-window**  
**9. Added Widevine installation function**  
**10. Fixed Waydroid Runner 1.0.0 unable to display main interface properly in Weston/Sway after installing Waydroid in X11 environment**  
11. Added function to set screen auto-rotation  
12. Added function to fix mouse display issue in Waydroid multi-window on some desktop environments  

### 1.0.0 (August 3, 2023)
**1. Added Waydroid main program installation function, image download function and domestic source**  
**2. Support for installing Magisk, Libhoudini (binary translator, can run ARM APK)**  
**3. Support for basic control of Waydroid**  
**4. Support for installing/uninstalling Android applications**  
**5. Provides app store to install APK**

## Source Code Installation Tutorial
```bash
git clone https://gitee.com/gfdgd-xi/waydroid-runner
cd waydroid-runner 
make install -j4
```

## Contributors
@Telegram HuskyDG for the solution to install `Magisk` to the `/system` partition and his `Magisk-Delta`  
@casualsuek for `Waydroid-Script` code    
@Quackdoc for Waydroid-Choose-gpu.sh  

# ©2023~Now gfdgd xi, Bail, LFRon

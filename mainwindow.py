#!/usr/bin/env python3
# 基于 GPLV3 开源
import os
import sys
import time
import json
import torch
import random
import threading
import traceback
import updatekiller
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from Model import *


def ReadWaydroidLog():
    if not os.path.exists("/var/lib/waydroid/waydroid.log"):
        QtWidgets.QMessageBox.critical(mainwindow, "错误", "无法正确读取 Waydroid 日志文件，请检查是否正常安装 Waydroid")
        return
    QtWidgets.QInputDialog.getMultiLineText(mainwindow, "Waydroid 日志", "", readtxt("/var/lib/waydroid/waydroid.log"))

# 读取文本文档
def readtxt(path: "路径")->"读取文本文档":
    f = open(path, "r")  # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

def WriteTxt(path: str, things: str):
    with open(path, "w") as file:
        file.write(things)

def GetSystemVersion():
    systemInformation = readtxt("/etc/os-release")
    for systemInformation in systemInformation.split('\n'):
        if "PRETTY_NAME=" in systemInformation:
            return systemInformation.replace("PRETTY_NAME=", "").replace('"', '')

def RunBash(bashCommand: str):
    # 因为 Terminal 读取的返回值肯定有问题，所以得用折中的方案
    tmpBashPath = f"/tmp/waydroid-runner-{random.randint(0, 1000)}.sh"
    WriteTxt(tmpBashPath, f"""#!/bin/bash
{bashCommand}
if [[ $? != 0 ]]; then
    zenity --error --text=脚本出现错误 --no-wrap
    exit 1
fi
zenity --info --text=执行成功！ --no-wrap""")
    OpenTerminal(f"bash '{tmpBashPath}'")
    os.remove(tmpBashPath)

def DisabledAndEnbled(status: bool):
    apkPath.setDisabled(status)
    apkPathBrowser.setDisabled(status)
    installButton.setDisabled(status)

class InstallApk(QtCore.QThread):
    info = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    combo = QtCore.pyqtSignal(int)

    def __init__(self, path, quit = False) -> None:
        self.path = path
        self.quit = quit
        super().__init__()
    
    def run(self):
        print(self.path)
        print(f"waydroid app install '{self.path}'")
        result = os.system(f"waydroid app install '{self.path}'")
        if result:
            self.error.emit("安装失败！请检查 Waydroid 安装正常以及是否支持该 APK")
            DisabledAndEnbled(False)
            return
        self.info.emit("安装成功！")
        DisabledAndEnbled(False)

def ErrorBox(error):
    QtWidgets.QMessageBox.critical(widget, "错误", error)

def InformationBox(info):
    QtWidgets.QMessageBox.information(widget, "提示", info)

def UpdateCombobox(tmp):
    pass

def InstallApkButton():
    global install
    DisabledAndEnbled(True)
    install = InstallApk(apkPath.currentText())
    install.info.connect(InformationBox)
    install.error.connect(ErrorBox)
    install.combo.connect(UpdateCombobox)
    install.start()


def BrowserApk():
    path = QtWidgets.QFileDialog.getOpenFileName(mainwindow, "选择APK", homePath, "APK 文件(*.apk);;所有文件(*.*)")
    if path[0] == "":
        return
    apkPath.setCurrentText(path[0])

# 关于窗口
helpWindow = None
def showhelp():
    global helpWindow
    helpWindow = QtWidgets.QMainWindow()
    helpWidget = QtWidgets.QWidget()
    helpLayout = QtWidgets.QGridLayout()

    def ChgLog():
        HelpStr.setHtml(updateThingsString)
    def ChgAbout(event):
        HelpStr.setHtml(about)
    def ChgCon():
        HelpStr.setHtml(contribute)
    def ChgTips():
        HelpStr.setHtml(tips)
    
    def ChgGPLV3():
        try:
            with open(f"{programPath}/LICENSE", "r") as file:
                things = file.read()
                try:
                    HelpStr.setMarkdown(things)
                except:
                    # 旧版 QT 不支持 Markdown
                    traceback.print_exc()
                    HelpStr.setText(things)
        except:
            traceback.print_exc()
            HelpStr.setText(traceback.print_exc())
    
    BtnReadme = QtWidgets.QPushButton("使用说明")
    BtnLog = QtWidgets.QPushButton("更新内容")
    BtnGongxian = QtWidgets.QPushButton("谢明列表")
    BtnAbout = QtWidgets.QPushButton("关于")
    BtnGPLV3 = QtWidgets.QPushButton("程序开源许可证")
    HelpStr = QtWidgets.QTextBrowser()
    # 此功能从 2.0.0 后不再隐藏
    #BtnDownN.setEnabled("--彩蛋" in sys.argv)
    BtnReadme.clicked.connect(ChgTips)
    BtnLog.clicked.connect(ChgLog)
    BtnGongxian.clicked.connect(ChgCon)
    BtnAbout.clicked.connect(ChgAbout)
    BtnGPLV3.clicked.connect(ChgGPLV3)

    ChgTips()

    helpLayout.addWidget(BtnReadme, 0, 0, 1, 1)
    helpLayout.addWidget(BtnLog, 1, 0, 1, 1)
    helpLayout.addWidget(BtnGongxian, 2, 0, 1, 1)
    helpLayout.addWidget(BtnGPLV3, 3, 0, 1, 1)
    helpLayout.addWidget(BtnAbout, 4, 0, 1, 1)
    helpLayout.addWidget(HelpStr, 0, 1, 10, 1)

    helpWidget.setLayout(helpLayout)
    helpWindow.setCentralWidget(helpWidget)
    helpWindow.setFixedSize(int(helpWindow.frameSize().width() * 0.9), int(helpWindow.frameSize().height() * 1.5))
    helpWindow.setWindowTitle(f"{windowTitle}——帮助")
    helpWindow.setWindowIcon(QtGui.QIcon(iconPath))
    helpWindow.show()
    return

# 环境变量
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
information = json.loads(readtxt(programPath + "/information.json"))
SystemVersion = GetSystemVersion()
programUrl = information["Url"][0]
version = information["Version"]
goodRunSystem = information["System"]
iconPath = "{}/runner.svg".format(os.path.split(os.path.realpath(__file__))[0])
updateThingsString = ""
homePath = os.getenv("HOME")
about = f'''<p align="center"><img width=256 src="{iconPath}"/></p>
<p>介绍：</p>
<p>程序开源许可证：GPLV3</p>
<p>版本：{version}</p>
<p>适用平台：{goodRunSystem}</p>
<p>Qt 版本：{QtCore.qVersion()}</p>
<p>程序官网：{programUrl}</p>
<p>系统版本：{SystemVersion}</p>
<p>安装包构建时间：{information['Time']}</p>
<h1>©2023-{time.strftime("%Y")}</h1>'''
tips = ""
contribute = ""
iconPath = f"{programPath}"
windowTitle = f"Waydroid 运行器 {version}"

app = QtWidgets.QApplication(sys.argv)
# 环境检测
if os.system("which waydroid"):
    if QtWidgets.QMessageBox.question(None, "提示", "您还未安装 Waydroid，是否立即安装？") == QtWidgets.QMessageBox.Yes:
        RunBash(f"bash '{programPath}/Runner_tools/Waydroid_Installer/Install.sh'")
        sys.exit()

# 窗口
mainwindow = QtWidgets.QMainWindow()
widget = QtWidgets.QWidget()
widgetLayout = QtWidgets.QGridLayout()
# 权重
size = QtWidgets.QSizePolicy()
size.setHorizontalPolicy(0)
### 创建控件
## 安装 apk
apkPath = QtWidgets.QComboBox()
apkPathBrowser = QtWidgets.QPushButton("浏览")
installButton = QtWidgets.QPushButton("安装")
# 设置属性
apkPath.setEditable(True)
apkPathBrowser.clicked.connect(BrowserApk)
installButton.clicked.connect(InstallApkButton)
apkPathBrowser.setSizePolicy(size)
installButton.setSizePolicy(size)
# layout
apkInstallLayout = QtWidgets.QHBoxLayout()
apkInstallLayout.addWidget(apkPath)
apkInstallLayout.addWidget(apkPathBrowser)
apkInstallLayout.addWidget(installButton)
## info
gpuDevice = QtWidgets.QLabel("当前工作GPU：AMD Raven Ridge")
gpuChooser = QtWidgets.QPushButton("选择")
waydroidStatus = QtWidgets.QLabel("Waydroid：已安装")
magiskDeltoInstallStatus = QtWidgets.QLabel("Magisk Delta：已安装")
libkoudiniInstallStatus = QtWidgets.QLabel("Libhoudini：已安装")
lsPosedInstallStatus = QtWidgets.QLabel("LSPosed：已安装")
diskUsing = QtWidgets.QLabel("存储占用：8.56GB")
memoryUsing = QtWidgets.QLabel("内存占用：850MB")
# layout
infoLayout = QtWidgets.QGridLayout()
infoLayout.addWidget(waydroidStatus, 0, 0, 1, 2)
infoLayout.addWidget(gpuDevice, 1, 0, 1, 2)
infoLayout.addWidget(gpuChooser, 1, 3)
infoLayout.addWidget(magiskDeltoInstallStatus, 2, 0)
infoLayout.addWidget(libkoudiniInstallStatus, 3, 0)
infoLayout.addWidget(diskUsing, 3, 1)
infoLayout.addWidget(lsPosedInstallStatus, 4, 0)
infoLayout.addWidget(memoryUsing, 4, 1)

## 大 layout
widgetLayout.addLayout(apkInstallLayout, 2, 0)
widgetLayout.addLayout(infoLayout, 3, 0)

widget.setLayout(widgetLayout)
mainwindow.setWindowTitle(windowTitle)
mainwindow.setCentralWidget(widget)
## 菜单栏
menu = mainwindow.menuBar()
programMenu = menu.addMenu("程序(&W)")
waydroidMenu = menu.addMenu("Waydroid(&W)")
configMenu = menu.addMenu("容器配置(&C)")
helpMenu = menu.addMenu("帮助(&H)")
# 程序栏
settingProgramAction = QtWidgets.QAction("设置程序")
exitProgramAction = QtWidgets.QAction("退出程序")
programMenu.addAction(settingProgramAction)
programMenu.addAction(exitProgramAction)
exitProgramAction.triggered.connect(sys.exit)
# Waydroid 栏
installWaydroidAction = QtWidgets.QAction("安装 Waydroid 本体")
waydroidLog = QtWidgets.QAction("查看 Waydroid 日志")

gpuChooseAction = QtWidgets.QAction("GPU 选择")
installWaydroidAction.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"bash '{programPath}/Runner_tools/Waydroid_Installer/Install.sh'"]))

waydroidLog.triggered.connect(ReadWaydroidLog)
waydroidMenu.addAction(installWaydroidAction)
waydroidMenu.addAction(waydroidLog)
waydroidMenu.addAction(gpuChooseAction)
# 容器配置栏
magiskInstall = QtWidgets.QAction("安装 Magisk")
waydroidLaguage = QtWidgets.QAction("设置 Waydroid 容器语言为中文")
multiWindowsSet = QtWidgets.QAction("开启 Waydroid 多窗口")
doNotRotate = QtWidgets.QAction("禁用在多窗口模式下最大化窗口屏幕方向自动旋转")
configMenu.addAction(magiskInstall)
configMenu.addSeparator()
configMenu.addAction(waydroidLaguage)
configMenu.addSeparator()
configMenu.addAction(multiWindowsSet)
configMenu.addAction(doNotRotate)
magiskInstall.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/Magisk_Installer/Magisk.py'"]).start())
waydroidLaguage.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"pkexec python3 '{programPath}/Runner_tools/SystemConfigs/Language.py'"]).start())
doNotRotate.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/SystemConfigs/Do-not-rotate.py'"]).start())
multiWindowsSet.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/SystemConfigs/Multi_windows.py'"]).start())
# 帮助 栏
helpAction = QtWidgets.QAction("程序帮助")
uploadBugAction = QtWidgets.QAction("问题反馈")
aboutThisProgramAction = QtWidgets.QAction("关于本程序(&A)")
helpAction.triggered.connect(showhelp)
aboutThisProgramAction.triggered.connect(showhelp)
helpMenu.addAction(helpAction)
helpMenu.addAction(uploadBugAction)
helpMenu.addAction(aboutThisProgramAction)

## 窗口属性
mainwindow.setWindowIcon(QtGui.QIcon(iconPath))

mainwindow.show()
mainwindow.resize(int(mainwindow.frameGeometry().width() * 1.8), int(mainwindow.frameGeometry().height()))

# 检测显卡型号
#ng = torch.cuda.device_count()
#print("Devices:%d" %ng)
#infos = [torch.cuda.get_device_properties(i) for i in range(ng)]
#print(infos)
#print(pynvml.nvmlDeviceGetCount())
#gpuDevice.setText(f"GPU 型号：{pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(0))}")
#deviceCount = pynvml.nvmlDeviceGetCount()

# 检测 Waydroid 是否存在
if os.system("which waydroid"):
    waydroidStatus.setText("Waydroid：未安装")
#os.system(f"ls {programPath}/Runner_tools/Checks/HoudiniCheck.py")
print(os.system(f"python3 '{programPath}/Runner_tools/Checks/HoudiniCheck.py'"))
libkoudiniInstallStatus.setText("Libhoudini：" + ["已安装", "未安装"][os.system(f"python3 '{programPath}/Runner_tools/Checks/HoudiniCheck.py'")>>8])
lsPosedInstallStatus.setText("LSPosed：" + ["已安装", "未安装"][os.system(f"python3 '{programPath}/Runner_tools/Checks/LSPCheck.py'")>>8])
magiskDeltoInstallStatus.setText("Magisk Delta：" + ["已安装", "未安装"][os.system(f"python3 '{programPath}/Runner_tools/Checks/MagiskCheck.py'")>>8])

#libkoudiniInstallStatus = QtWidgets.QLabel("Libhoudini：已安装")

sys.exit(app.exec_())
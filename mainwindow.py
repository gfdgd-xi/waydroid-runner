#!/usr/bin/env python3
# 依据 GPLV3 开源
import os
import sys
import time
import json
import numpy
import base64
import shutil
import random
import zipfile
import requests
import threading
import traceback
import webbrowser
import subprocess
import matplotlib
import updatekiller
import urllib.parse as parse
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from getxmlimg import getsavexml
from Model import *

# 需引入 subprocess
# 运行系统命令并获取返回值
def GetCommandReturn(cmd: "命令")->"运行系统命令并获取返回值":
    # cmd 是要获取输出的命令
    return subprocess.getoutput(cmd)

# 获取 aapt 的所有信息
def GetApkInformation(apkFilePath: "apk 所在路径")->"获取 aapt 的所有信息":
    return GetCommandReturn("aapt dump badging '{}'".format(apkFilePath))

# 获取 apk 包名
def GetApkPackageName(apkFilePath: "apk 所在路径")->"获取 apk 包名":
    info = GetApkInformation(apkFilePath)
    for line in info.split('\n'):
        if "package:" in line:
            line = line[0: line.index("versionCode='")]
            line = line.replace("package:", "")
            line = line.replace("name=", "")
            line = line.replace("'", "")
            line = line.replace(" ", "")
            return line

# 读取 Waydroid 日志
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
    rm '{tmpBashPath}' -f
    exit 1
fi
zenity --info --text=执行成功！ --no-wrap
rm '{tmpBashPath}' -f""")
    OpenTerminal(f"bash '{tmpBashPath}'")
    #os.remove(tmpBashPath)

def DisabledAndEnbled(status: bool):
    apkPath.setDisabled(status)
    apkPathBrowser.setDisabled(status)
    installButton.setDisabled(status)
    removeButton.setDisabled(status)

class UninstallApk(QtCore.QThread):
    info = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    combo = QtCore.pyqtSignal(int)
    def __init__(self, package) -> None:
        self.package = package
        super().__init__()

    def run(self):
        global findApkHistory
        result = os.system(f"waydroid app remove '{self.package}'")
        if result:
            self.error.emit(f"卸载失败！请检查 Waydroid 安装正常以及选择 APK 对应包名是否存在/输入包名存在\n命令返回值：{result}")
            DisabledAndEnbled(False)
            return
        try:
            if findApkHistory[-1] != apkPath.currentText():
                findApkHistory.append(apkPath.currentText())
        except:
            findApkHistory.append(apkPath.currentText())
        self.combo.emit(0)
        try:
            WriteTxt(homePath + "/.config/waydroid-runner/FindApkHistory.json", str(json.dumps(ListToDictionary(findApkHistory))))  # 将历史记录的数组转换为字典并写入
        except:
            traceback.print_exc()
            self.error.emit(traceback.format_exc())
        self.info.emit("执行完成！若卸载成功则会在一段时间后自动在启动器移除 .desktop 文件")
        DisabledAndEnbled(False)

# 数组转字典
def ListToDictionary(list: "需要转换的数组")->"数组转字典":
    dictionary = {}
    for i in range(len(list)):
        dictionary[i] = list[i]
    return dictionary     

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
        result = os.system(f"waydroid app install '{self.path}'")>>8
        if result:
            self.error.emit(f"安装失败！请检查 Waydroid 安装正常以及是否支持该 APK\n命令返回值：{result}")
            DisabledAndEnbled(False)
            return
        try:
            if findApkHistory[-1] != apkPath.currentText():
                findApkHistory.append(apkPath.currentText())
        except:
            findApkHistory.append(apkPath.currentText())
        self.combo.emit(0)
        try:
            WriteTxt(homePath + "/.config/waydroid-runner/FindApkHistory.json", str(json.dumps(ListToDictionary(findApkHistory))))  # 将历史记录的数组转换为字典并写入
        except:
            traceback.print_exc()
            self.error.emit(traceback.format_exc())
        self.info.emit("执行完成！若安装成功则会在一段时间后自动在启动器生成 .desktop 文件")
        DisabledAndEnbled(False)

def ErrorBox(error):
    QtWidgets.QMessageBox.critical(widget, "错误", error)

def InformationBox(info):
    QtWidgets.QMessageBox.information(widget, "提示", info)

def UpdateCombobox(tmp):
    apkPath.clear()
    apkPath.addItems(findApkHistory)
    try:
        apkPath.setEditText(findApkHistory[-1])
    except:
        pass

def UninstallApkButton():
    global install
    DisabledAndEnbled(True)
    package = apkPath.currentText()
    if os.path.exists(package):
        package = GetApkPackageName(package)
    install = UninstallApk(package)
    install.info.connect(InformationBox)
    install.error.connect(ErrorBox)
    install.combo.connect(UpdateCombobox)
    install.start()

def InstallApkButton():
    global install
    DisabledAndEnbled(True)
    install = InstallApk(apkPath.currentText())
    install.info.connect(InformationBox)
    install.error.connect(ErrorBox)
    install.combo.connect(UpdateCombobox)
    install.start()

# 浏览 apk
def BrowserApk():
    path = QtWidgets.QFileDialog.getOpenFileName(mainwindow, "选择APK", json.loads(readtxt(homePath + "/.config/waydroid-runner/FindApk.json"))["path"], "APK 文件(*.apk);;所有文件(*.*)")
    if path[0] == "":
        return
    apkPath.setCurrentText(path[0])
    try:
        WriteTxt(homePath + "/.config/waydroid-runner/FindApk.json", json.dumps({"path": os.path.dirname(path)}))  # 写入配置文件
    except:
        pass

# 获取软件的中文名称
def GetApkChineseLabel(apkFilePath)->"获取软件的中文名称":
    info = GetApkInformation(apkFilePath)
    name = None
    for line in info.split('\n'):
        if "application-label-zh:" in line:
            line = line.replace("application-label-zh:", "")
            line = line.replace("'", "")
            return line
        if "application-label:" in line:
            line = line.replace("application-label:", "")
            line = line.replace("'", "")
            name = line
    return name

# 检测是否在 Wayland 下运行程序
def CheckWaylandRun(waylandUnShow=False):
    if os.getenv("XDG_SESSION_TYPE") == "x11":
        QtWidgets.QMessageBox.warning(mainwindow, "警告", "当前您使用的是 X11 桌面环境，而 Waydroid 需要在 Wayland 环境下运行\n请你使用支持 Wayland 的桌面环境并开启 Wayland 支持或使用 Sway 或 Weston 运行\n目前运行器支持自动开启 Sway 或 Weston 运行 Waydroid")
    if not waylandUnShow:
        QtWidgets.QMessageBox.information(mainwindow, "提示", "您当前在 Wayland 环境")

# 保存apk图标
def SaveApkIcon(apkFilePath, iconSavePath)->"保存 apk 文件的图标":
    try:
        if os.path.exists(iconSavePath):
            os.remove(iconSavePath)
        info = GetApkInformation(apkFilePath)
        for line in info.split('\n'):
            if "application:" in line:
                xmlpath = line.split(":")[-1].split()[-1].split("=")[-1].replace("'","")  
                if xmlpath.endswith('.xml'):
                        xmlsave = getsavexml()
                        print(xmlpath)
                        xmlsave.savexml(apkFilePath,xmlpath,iconSavePath)
                        return
                else:
                    zip = zipfile.ZipFile(apkFilePath)
                    iconData = zip.read(xmlpath)
                    with open(iconSavePath, 'w+b') as saveIconFile:
                        saveIconFile.write(iconData)
                        return
        print("None Icon! Show defult icon")
        shutil.copy(programPath + "/defult.svg", iconSavePath)
    except:
        traceback.print_exc()
        print("Error, show defult icon")
        shutil.copy(programPath + "/defult.svg", iconSavePath)

# 获取 apk Activity
def GetApkActivityName(apkFilePath: "apk 所在路径")->"获取 apk Activity":
    info = GetApkInformation(apkFilePath)
    for line in info.split('\n'):
        if "launchable-activity" in line:
            line = line[0: line.index("label='")]
            line = line.replace("launchable-activity: ", "")
            line = line.replace("'", "")
            line = line.replace(" ", "")
            line = line.replace("name=", "")
            line = line.replace("label=", "")
            line = line.replace("icon=", "")
            return line
    return f"{GetApkPackageName(apkFilePath)}.Main"

# 更新窗口
class UpdateWindow():
    data = {}
    update = None
    def ShowWindow():
        UpdateWindow.update = QtWidgets.QMainWindow()
        updateWidget = QtWidgets.QWidget()
        updateWidgetLayout = QtWidgets.QGridLayout()
        versionLabel = QtWidgets.QLabel(f"当前版本：{version}\n最新版本：未知\n更新内容：")
        updateText = QtWidgets.QTextBrowser()
        ok = QtWidgets.QPushButton("更新（更新过程中会关闭这个应用的所有进程）")
        ok.clicked.connect(UpdateWindow.Update)
        cancel = QtWidgets.QPushButton("取消")
        cancel.clicked.connect(UpdateWindow.update.close)
        ok.setDisabled(True)
        try:
            UpdateWindow.data = json.loads(requests.get("http://update.gfdgdxi.top/waydroid-runner/update.json").text)
            versionLabel = QtWidgets.QLabel(f"当前版本：{version}\n最新版本：{UpdateWindow.data['Version']}\n更新内容：")
            if UpdateWindow.data["Version"] == version:
                updateText.setText("此为最新版本，无需更新")
                ok.setDisabled(True)
            else:
                # 版本号读取（防止出现高版本号提示要“升级”到低版本号的问题）
                localVersionList = version.split(".")
                webVersionList = UpdateWindow.data['Version'].split(".")
                for i in range(len(localVersionList)):
                    local = int(localVersionList[i])
                    web = int(webVersionList[i])
                    if web < local:
                        updateText.setHtml(f"""<p>此为最新版本，无需更新，但似乎您当前使用的程序版本比云端版本还要高。</p>
<p>出现这个问题可能会有如下几种情况：</p>
<p>1、使用编译或者内测版本</p>
<p>2、自己修改了程序版本</p>
<p>3、作者忘记更新云端上的更新信息了</p>
<p>如果是第三种情况，请反馈到此：https://gitee.com/gfdgd-xi/waydroid-runner/issues/I7JVH7</p>
<p><img src='{programPath}/Icon/doge.png'></p>""")
                        ok.setDisabled(True)
                        break
                    if web > local:
                        updateText.setText(UpdateWindow.data["New"].replace("\\n", "\n"))
                        ok.setEnabled(True)
                        break
                
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(updateWidget, "错误", "无法连接服务器！")
        updateWidgetLayout.addWidget(versionLabel, 0, 0, 1, 1)
        updateWidgetLayout.addWidget(updateText, 1, 0, 1, 3)
        updateWidgetLayout.addWidget(ok, 2, 2, 1, 1)
        updateWidgetLayout.addWidget(cancel, 2, 1, 1, 1)
        updateWidget.setLayout(updateWidgetLayout)
        UpdateWindow.update.setCentralWidget(updateWidget)
        UpdateWindow.update.setWindowTitle("检查 Waydroid 运行器更新")
        UpdateWindow.update.setWindowIcon(QtGui.QIcon(iconPath))
        UpdateWindow.update.resize(updateWidget.frameGeometry().width(), int(updateWidget.frameGeometry().height() * 1.5))
        UpdateWindow.update.show()

    def Update():
        if os.path.exists("/tmp/waydroid-runner/update"):
            shutil.rmtree("/tmp/waydroid-runner/update")
        os.makedirs("/tmp/waydroid-runner/update")
        try:            
            print(UpdateWindow.data["Url"])
            WriteTxt("/tmp/waydroid-runner/update.sh", f"""#!/bin/bash
echo 删除多余的安装包
rm -rfv /tmp/waydroid-runner/update/*
echo 关闭“Waydroid 运行器”
python3 "{programPath}/updatekiller.py"
echo 下载安装包
wget -P /tmp/waydroid-runner/update {UpdateWindow.data["Url"][0]}
echo 安装安装包
dpkg -i /tmp/waydroid-runner/update/*
echo 修复依赖关系
apt install -f -y
notify-send -i "{iconPath}" "更新完毕！"
zenity --info --text=\"更新完毕！\" --ellipsize
""")
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(widget, "错误，无法继续更新", traceback.format_exc())
        OpenTerminal(f"pkexec bash /tmp/waydroid-runner/update.sh")
        

# 获取 APK 版本
def GetApkVersion(apkFilePath):
    info = GetApkInformation(apkFilePath)
    for line in info.split('\n'):
        if "package:" in line:
            if "compileSdkVersion='" in line:
                line = line.replace(line[line.index("compileSdkVersion='"): -1], "")
            if "platform" in line:
                line = line.replace(line[line.index("platform"): -1], "")
            line = line.replace(line[0: line.index("versionName='")], "")
            line = line.replace("versionName='", "")
            line = line.replace("'", "")
            line = line.replace(" ", "")
            return line

image = None
class ApkInformation():
    message = None
    def ShowWindows():
        global fullInformation
        global path
        global tab1
        path = apkPath.currentText()
        if os.system("which aapt") >> 8:
            QtWidgets.QMessageBox.critical(widget, "错误", "系统未安装 aapt")
            return
        package = GetApkPackageName(path)
        if package == None or package == "":
            QtWidgets.QMessageBox.critical(widget, "错误", "APK 文件不存在或错误！")
            return
        ApkInformation.message = QtWidgets.QMainWindow()
        messageWidget = QtWidgets.QWidget()
        messageLayout = QtWidgets.QVBoxLayout()
        ApkInformation.message.setWindowTitle("“{}“的Apk信息".format(GetApkChineseLabel(path)))
        tab = QtWidgets.QTabWidget()

        tab1 = QtWidgets.QWidget()
        tab2 = QtWidgets.QWidget()

        tab.addTab(tab1, "简化版")
        tab1Layout = QtWidgets.QGridLayout()
        SaveApkIcon(path, "/tmp/waydroid-runner-android-app-icon.png")
        simpleInformation = QtWidgets.QLabel(f"""
<p align='center'><img width='256' src='/tmp/waydroid-runner-android-app-icon.png'></p>
<p>包名：{GetApkPackageName(path)}</p>
<p>中文名：{GetApkChineseLabel(path)}</p>
<p>Activity：{GetApkActivityName(path)}</p>
<p>版本：{GetApkVersion(path)}</p>""")

        seeFen = QtWidgets.QPushButton("查看程序评分情况")
        updFen = QtWidgets.QPushButton("上传程序评分情况")
        #seeFen.setEnabled(map)
        seeFen.clicked.connect(ApkInformation.ShowMap)
        updFen.clicked.connect(ApkInformation.UpdateMark)
        tab1Layout.addWidget(simpleInformation, 0, 0, 1, 3)
        tab1Layout.addWidget(seeFen, 1, 1, 1, 1)
        tab1Layout.addWidget(updFen, 2, 1, 1, 1)
        tab1.setLayout(tab1Layout)

        tab.addTab(tab2, "完整版")
        tab2Layout = QtWidgets.QVBoxLayout()
        fullInformation = QtWidgets.QTextBrowser()
        fullInformation.setText(GetApkInformation(path))
        tab2Layout.addWidget(fullInformation)
        tab2.setLayout(tab2Layout)

        messageLayout.addWidget(tab)
        messageWidget.setLayout(messageLayout)
        ApkInformation.message.setCentralWidget(messageWidget)
        ApkInformation.message.setWindowIcon(QtGui.QIcon(iconPath))
        ApkInformation.message.setWindowTitle("APK 信息")
        ApkInformation.message.show()
        return

    def UpdateMark():
        chooseWindow = QtWidgets.QMessageBox()
        chooseWindow.setWindowTitle("选择评分")
        chooseWindow.setText(f"""选择应用“{GetApkChineseLabel(path)}”的使用评分。建议参考如下规范进行评分：
含有不良信息（-1分）：含有违法违规信息（如果有就不要选择其它选项了）
0星：完全无法使用，连安装都有问题
1星：完全无法使用，但是能正常安装
2星：可以打开，但只能使用一点点功能
3星：勉强能使用，运行也不大流畅
4星：大部分功能正常，运行流畅（可能会有点小卡）
5星：完全正常且非常流畅，没有任何功能和性能问题，就和直接在手机上用一样
""")
        choices=["含有不良信息", "0分", "1分", "2分", "3分", "4分", "5分", "取消"]
        button0 = chooseWindow.addButton(choices[0], QtWidgets.QMessageBox.ActionRole)
        button1 = chooseWindow.addButton(choices[1], QtWidgets.QMessageBox.ActionRole)
        button2 = chooseWindow.addButton(choices[2], QtWidgets.QMessageBox.ActionRole)
        button3 = chooseWindow.addButton(choices[3], QtWidgets.QMessageBox.ActionRole)
        button4 = chooseWindow.addButton(choices[4], QtWidgets.QMessageBox.ActionRole)
        button5 = chooseWindow.addButton(choices[5], QtWidgets.QMessageBox.ActionRole)
        button6 = chooseWindow.addButton(choices[6], QtWidgets.QMessageBox.ActionRole)
        button7 = chooseWindow.addButton(choices[7], QtWidgets.QMessageBox.ActionRole)
        button0.clicked.connect(lambda: ApkInformation.UpdateMarkInternet(int(0)))
        button1.clicked.connect(lambda: ApkInformation.UpdateMarkInternet(int(1)))
        button2.clicked.connect(lambda: ApkInformation.UpdateMarkInternet(int(2)))
        button3.clicked.connect(lambda: ApkInformation.UpdateMarkInternet(int(3)))
        button4.clicked.connect(lambda: ApkInformation.UpdateMarkInternet(int(4)))
        button5.clicked.connect(lambda: ApkInformation.UpdateMarkInternet(int(5)))
        button6.clicked.connect(lambda: ApkInformation.UpdateMarkInternet(int(6)))
        button7.clicked.connect(lambda: ApkInformation.UpdateMarkInternet(int(7)))
        chooseWindow.exec_()
        return
    
    def UpdateMarkInternet(choose):
        print(choose)
        if choose == None or choose == 7:
            return
        
        try:
            QtWidgets.QMessageBox.information(widget, "提示", requests.post(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3VlbmdpbmUtcnVubmVyL2FwcC9jaGVjay9hZGQucGhw"), {"Package": GetApkPackageName(path), "Type": choose}).text)
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(widget, "错误", "无法连接服务器！")


    def ShowMap():
        package = GetApkPackageName(path)
        if package == None or package == "":
            QtWidgets.QMessageBox.critical(widget, "错误", "APK 不存在或错误")
            return
        try:
            data = json.loads(requests.get("http://data.download.gfdgdxi.top/uengineapp/" + package +"/data.json").text)
            print(data)
        except:
            QtWidgets.QMessageBox.information(widget, "提示", "此程序暂时没有评分，欢迎您贡献第一个评分！")
            return
        index = numpy.arange(len(data))
        print(index)
        chinese = GetApkChineseLabel(path)
        fig = matplotlib.pylab.figure()
        fig.canvas.set_window_title("“" + chinese + "”的用户评分（数据只供参考）")
        fonts = matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')  # 用于支持中文显示，需要依赖fonts-noto-cjk
        matplotlib.pylab.barh(index, data)
        matplotlib.pylab.yticks(index, ["不良信息", "0分", "1分", "2分", "3分", "4分", "5分"], fontproperties=fonts)
        matplotlib.pylab.xlabel("用户评分数", fontproperties=fonts)
        matplotlib.pylab.ylabel("等级", fontproperties=fonts)
        matplotlib.pylab.title("“" + chinese + "”的用户评分（数据只供参考）", fontproperties=fonts)
        matplotlib.pylab.show(block=True)

# 用户自行保存
def SaveIconToOtherPath():
    apkPath = apkPath.currentText()
    if apkPath == "":
        QtWidgets.QMessageBox.critical(widget, "错误", "APK 不存在或错误")
        return
    path = QtWidgets.QFileDialog.getSaveFileName(widget, "保存图标", "icon.png", "PNG 图片(*.png);;所有文件(*.*)", json.loads(readtxt(homePath + "/.config/waydroid-runner/SaveApkIcon.json"))["path"])[0]
    if not path == "":
        try:
            SaveApkIcon(apkPath, path)
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(widget, "错误", "图标保存失败！")
            return
        #WriteTxt(homePath + "/.config/uengine-runner/SaveApkIcon.json", json.dumps({"path": os.path.dirname(path)}))  # 写入配置文件
        #findApkHistory.append(ComboInstallPath.currentText())
        UpdateCombobox(0)
        #WriteTxt(homePath + "/.config/uengine-runner/FindApkHistory.json", str(json.dumps(ListToDictionary(findApkHistory))))  # 将历史记录的数组转换为字典并写入
        QtWidgets.QMessageBox.information(widget, "提示", "保存成功！")

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
<p>介绍：Waydroid运行器是可以通过GUI形式半自动配置Waydroid的工具，使用户使用Waydroid更为方便。Waydroid本身存在很多因AOSP未考虑PC用户而产生的问题(如没有自带Houdini,默认英语,默认非小窗模式)而使用户使用起来非常难受,本运行器支持以GUI形式自动化安装以及配置Waydroid，并会创建快捷控制的快捷方式，可以用于玩游戏/刷视频/Android开发等。</p>
<p>程序开源许可证：GPLV3</p>
<p>版本：{version}</p>
<p>适用平台：{goodRunSystem}</p>
<p>Qt 版本：{QtCore.qVersion()}</p>
<p>程序官网：{programUrl}</p>
<p>系统版本：{SystemVersion}</p>
<p>安装包构建时间：{information['Time']}</p>
<p>QQ 群：872491938</p>
<h1>©2023-{time.strftime("%Y")} gfdgd xi、Bail、LFRon</h1>'''
tips = ""
contribute = ""
for i in information["Tips"]:
    tips += f"<p>{i}</p>"
for i in information["Update"]:
    updateThingsString += f"<p>{i}</p>"
for i in information["Contribute"]:
    contribute += f"<p>{i}</p>"
iconPath = f"{programPath}"
windowTitle = f"Waydroid 运行器 {version}"

###########################
# 加载配置
###########################
app = QtWidgets.QApplication(sys.argv)
if not os.path.exists(homePath + "/.config/waydroid-runner"):  # 如果没有配置文件夹
    os.makedirs(homePath + "/.config/waydroid-runner")  # 创建配置文件夹
if not os.path.exists(homePath + "/.config/waydroid-runner/FindApkHistory.json"):  # 如果没有配置文件
    WriteTxt(homePath + "/.config/waydroid-runner/FindApkHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(homePath + "/.config/waydroid-runner/FindApkNameHistory.json"):  # 如果没有配置文件
    WriteTxt(homePath + "/.config/waydroid-runner/FindApkNameHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(homePath + "/.config/waydroid-runner/FindApkActivityHistory.json"):  # 如果没有配置文件
    WriteTxt(homePath + "/.config/waydroid-runner/FindApkActivityHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(homePath + "/.config/waydroid-runner/FindUninstallApkHistory.json"):  # 如果没有配置文件
    WriteTxt(homePath + "/.config/waydroid-runner/FindUninstallApkHistory.json", json.dumps({}))  # 创建配置文件
if not os.path.exists(homePath + "/.config/waydroid-runner/FindApkName.json"):  # 如果没有配置文件
    WriteTxt(homePath + "/.config/waydroid-runner/FindApkName.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(homePath + "/.config/waydroid-runner/FindApk.json"):  # 如果没有配置文件
    WriteTxt(homePath + "/.config/waydroid-runner/FindApk.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(homePath + "/.config/waydroid-runner/FindUninstallApk.json"):  # 如果没有配置文件
    WriteTxt(homePath + "/.config/waydroid-runner/FindUninstallApk.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(homePath + "/.config/waydroid-runner/SaveApkIcon.json"):  # 如果没有配置文件
    WriteTxt(homePath + "/.config/waydroid-runner/SaveApkIcon.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(homePath + "/.config/waydroid-runner/SaveApk.json"):  # 如果没有配置文件
    WriteTxt(homePath + "/.config/waydroid-runner/SaveApk.json", json.dumps({"path": "~"}))  # 写入（创建）一个配置文件
if not os.path.exists(homePath + "/.config/waydroid-runner/setting.json"):
    WriteTxt(homePath + "/.config/waydroid-runner/setting.json", json.dumps({"SaveApk": int(1)}))

defultProgramList = {
    "SaveApk": 1,
    "AutoScreenConfig": False,
    "ChooseProgramType": False,
    "Theme": ""
}
try:
    settingConf = json.loads(readtxt(homePath + "/.config/waydroid-runner/setting.json"))
    change = False
    for i in defultProgramList.keys():
        if not i in settingConf:
            change = True
            settingConf[i] = defultProgramList[i]
    if change:
        WriteTxt(homePath + "/.config/waydroid-setting.json", json.dumps(settingConf))
except:
    traceback.print_exc()
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QMessageBox.critical(None, "错误", f"无法读取配置，无法继续\n{traceback.format_exc()}")
    sys.exit(1)

findApkHistory = list(json.loads(readtxt(homePath + "/.config/waydroid-runner/FindApkHistory.json")).values())
fineUninstallApkHistory = list(json.loads(readtxt(homePath + "/.config/waydroid-runner/FindUninstallApkHistory.json")).values())
findApkNameHistory = list(json.loads(readtxt(homePath + "/.config/waydroid-runner/FindApkNameHistory.json")).values())
findApkActivityHistory = list(json.loads(readtxt(homePath + "/.config/waydroid-runner/FindApkActivityHistory.json")).values())

# 环境检测

if os.system("which waydroid"):
    if QtWidgets.QMessageBox.question(None, "提示", "您还未安装 Waydroid，是否立即安装？") == QtWidgets.QMessageBox.Yes:
        RunBash(f"bash '{programPath}/Runner_tools/Waydroid_Installer/Install-cn.sh'")
        sys.exit()

try:
    threading.Thread(target=requests.get, args=[parse.unquote(base64.b64decode("aHR0cDovLzEyMC4yNS4xNTMuMTQ0L3dheWRyb2lkLXJ1bm5lci9vcGVuL0luc3RhbGwucGhw").decode("utf-8")) + "?Version=" + version]).start()
except:
    pass

# 窗口
mainwindow = QtWidgets.QMainWindow()
CheckWaylandRun(True)
widget = QtWidgets.QWidget()
widgetLayout = QtWidgets.QGridLayout()
# 权重
size = QtWidgets.QSizePolicy()
size.setHorizontalPolicy(0)
### 创建控件
## 安装 apk
apkPath = QtWidgets.QComboBox()
appStore = QtWidgets.QPushButton("应用商店")
apkPathBrowser = QtWidgets.QPushButton("浏览")
installButton = QtWidgets.QPushButton("安装")
removeButton = QtWidgets.QPushButton("卸载")
infoButton = QtWidgets.QPushButton("详情")
saveIcon = QtWidgets.QPushButton("保存图标")
# 设置属性
apkPath.setEditable(True)
apkPathBrowser.clicked.connect(BrowserApk)
installButton.clicked.connect(InstallApkButton)
removeButton.clicked.connect(UninstallApkButton)
infoButton.clicked.connect(ApkInformation.ShowWindows)
saveIcon.clicked.connect(SaveIconToOtherPath)
appStore.clicked.connect(lambda: threading.Thread(target=os.system, args=[f"python3 '{programPath}/AutoConfig.py'"]).start())
apkPathBrowser.setSizePolicy(size)
installButton.setSizePolicy(size)
appStore.setSizePolicy(size)
# layout
apkInstallLayout = QtWidgets.QGridLayout()
apkInstallLayout.addWidget(apkPath, 0, 0, 1, 2)
apkInstallLayout.addWidget(appStore, 1, 0)
apkInstallLayout.addWidget(apkPathBrowser, 0, 2)
apkInstallLayout.addWidget(installButton, 0, 3)
apkInstallLayout.addWidget(removeButton, 1, 2)
apkInstallLayout.addWidget(infoButton, 1, 3)
apkInstallLayout.addWidget(saveIcon, 2, 2)
## info
waydroidStatus = QtWidgets.QLabel("Waydroid：已安装")
magiskDeltaInstallStatus = QtWidgets.QLabel("Magisk Delta：已安装")
libkoudiniInstallStatus = QtWidgets.QLabel("Libhoudini：已安装")
lsPosedInstallStatus = QtWidgets.QLabel("LSPosed：已安装")
wideVineInstallStatus = QtWidgets.QLabel("Widevine：已安装")
# layout
infoLayout = QtWidgets.QGridLayout()
infoLayout.addWidget(QtWidgets.QLabel("<hr><p><b>Waydroid 信息：</b></p>"), 0, 0, 1, 2)
infoLayout.addWidget(waydroidStatus, 1, 0)
infoLayout.addWidget(magiskDeltaInstallStatus, 1, 1)
infoLayout.addWidget(lsPosedInstallStatus, 2, 0)
infoLayout.addWidget(libkoudiniInstallStatus, 2, 1)
infoLayout.addWidget(wideVineInstallStatus, 3, 0)


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
#settingProgramAction = QtWidgets.QAction("设置程序")
checkWayland = QtWidgets.QAction("检测是否是在 Wayland 下运行该程序")
installSway = QtWidgets.QAction("安装 Sway")
installWeston = QtWidgets.QAction("安装 Weston")
exitProgramAction = QtWidgets.QAction("退出程序")
#programMenu.addAction(settingProgramAction)
programMenu.addAction(checkWayland)
programMenu.addSeparator()
programMenu.addAction(installSway)
programMenu.addAction(installWeston)
programMenu.addSeparator()
programMenu.addAction(exitProgramAction)
checkWayland.triggered.connect(CheckWaylandRun)
exitProgramAction.triggered.connect(sys.exit)
# Waydroid 栏
waydroidAutoSetting = QtWidgets.QAction("一键安装/设置 Waydroid")
waydroidAutoSetting.setDisabled(True)
installWaydroidCNAction = QtWidgets.QAction("安装 Waydroid 本体（国内源）")
installWaydroidAction = QtWidgets.QAction("安装 Waydroid 本体（官方源）")
waydroidStatus = QtWidgets.QAction("Waydroid 状态")
waydroidLog = QtWidgets.QAction("查看 Waydroid 日志")
restartWaydroidContainer = QtWidgets.QAction("重启 Waydroid 服务进程")
iconManager = QtWidgets.QAction("快捷方式管理工具")
waydroidRemoveAllDesktop = QtWidgets.QAction("移除所有 Waydroid 快捷方式")
waydroidShowFullUI = QtWidgets.QAction("显示 Waydroid Android 完整界面")
waydroidChangeGPU = QtWidgets.QAction("切换 GPU")
waydroidMenu.addAction(waydroidAutoSetting)
waydroidMenu.addSeparator()
waydroidMenu.addAction(installWaydroidCNAction)
waydroidMenu.addAction(installWaydroidAction)
waydroidMenu.addSeparator()
waydroidMenu.addAction(waydroidStatus)
waydroidMenu.addAction(waydroidLog)
waydroidMenu.addSeparator()
waydroidMenu.addAction(restartWaydroidContainer)
waydroidSession = waydroidMenu.addMenu("Waydroid Session")
waydroidSessionStart = QtWidgets.QAction("开启")
waydroidSessionStop = QtWidgets.QAction("关闭")
waydroidSessionStart.triggered.connect(lambda: threading.Thread(target=os.system, args=["waydroid session start && zenity --info --text=运行完成！ --no-wrap"]).start())
waydroidSessionStop.triggered.connect(lambda: threading.Thread(target=os.system, args=["waydroid session stop && zenity --info --text=运行完成！ --no-wrap"]).start())
waydroidSession.addAction(waydroidSessionStart)
waydroidSession.addAction(waydroidSessionStop)
waydroidMenu.addSeparator()
waydroidMenu.addAction(iconManager)
waydroidMenu.addAction(waydroidRemoveAllDesktop)
waydroidMenu.addSeparator()
waydroidMenu.addAction(waydroidShowFullUI)
waydroidMenu.addSeparator()
waydroidMenu.addAction(waydroidChangeGPU)
waydroidAutoSetting.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/auto-setting.py'"]).start())
installWaydroidCNAction.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"bash '{programPath}/Runner_tools/Waydroid_Installer/Install-cn.sh'"]).start())
installWaydroidAction.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"bash '{programPath}/Runner_tools/Waydroid_Installer/Install.sh'"]))
waydroidStatus.triggered.connect(lambda: QtWidgets.QInputDialog.getMultiLineText(mainwindow, "Waydroid 状态", "", subprocess.getoutput("waydroid status")))
waydroidLog.triggered.connect(ReadWaydroidLog)
restartWaydroidContainer.triggered.connect(lambda: os.system("systemctl restart waydroid-container.service && zenity --info --text=运行完成！ --no-wrap"))
iconManager.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"python3 '{programPath}/BuildDesktop.py'"]).start())
waydroidRemoveAllDesktop.triggered.connect(lambda: os.system("rm ~/.local/share/applications/waydroid.*.desktop -fv && zenity --info --text=删除完成！ --no-wrap"))
waydroidShowFullUI.triggered.connect(lambda: os.system("waydroid show-full-ui"))
waydroidChangeGPU.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"bash '{programPath}/Runner_tools/SystemConfigs/waydroid-choose-gpu.sh'"]).start())
# 容器配置栏
downloadImageCN = QtWidgets.QAction("下载 Waydroid 容器镜像")
magiskInstall = QtWidgets.QAction("安装 Magisk")
libhoudiniInstall = QtWidgets.QAction("安装 Libhoudini 翻译器")
widevineInstall = QtWidgets.QAction("安装 Widevine")
waydroidLaguage = QtWidgets.QAction("设置 Waydroid 容器语言为中文")
#multiWindowsSet = QtWidgets.QAction("开启 Waydroid 多窗口")
#doNotRotate = QtWidgets.QAction("")
waydroidAppListShow = QtWidgets.QAction("显示 Waydroid 安装的所有应用")
waydroidUpgradImage = QtWidgets.QAction("升级 Waydroid 容器（只限使用官方镜像安装方法）")
waydroidShell = QtWidgets.QAction("进入 Waydroid Shell")
#configMenu.addAction(downloadImageCN)
#configMenu.addSeparator()
configMenu.addAction(magiskInstall)
configMenu.addAction(libhoudiniInstall)
configMenu.addAction(widevineInstall)
configMenu.addSeparator()
configMenu.addAction(waydroidLaguage)
configMenu.addSeparator()
#configMenu.addAction(multiWindowsSet)
multiWindowsSet = configMenu.addMenu("设置 Waydroid 多窗口")
multiWindowsSetTips0 = QtWidgets.QAction("注：启用该功能后可能出现无法正常显示主界面的问题")
multiWindowsSetTips1 = QtWidgets.QAction("目前只支持部分桌面环境，不支持 Sway/Weston")
multiWindowsSetOn = QtWidgets.QAction("开启多窗口")
multiWindowsSetOff = QtWidgets.QAction("关闭多窗口")
multiWindowsSetTips0.setDisabled(True)
multiWindowsSetTips1.setDisabled(True)
multiWindowsSet.addAction(multiWindowsSetTips0)
multiWindowsSet.addAction(multiWindowsSetTips1)
multiWindowsSet.addSeparator()
multiWindowsSet.addAction(multiWindowsSetOn)
multiWindowsSet.addAction(multiWindowsSetOff)
#configMenu.addAction(doNotRotate)
doNotRotate = configMenu.addMenu("设置屏幕方向自动旋转")
doNotRotateTips = QtWidgets.QAction("此功能默认开启")
doNotRotateOn = QtWidgets.QAction("开启")
doNotRotateOff = QtWidgets.QAction("关闭")
doNotRotateTips.setDisabled(True)
doNotRotate.addAction(doNotRotateTips)
doNotRotate.addSeparator()
doNotRotate.addAction(doNotRotateOn)
doNotRotate.addAction(doNotRotateOff)
doNotRotateOn.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/Off-function/Allow-rotate.py'"]).start())
doNotRotateOff.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/SystemConfigs/Do-not-rotate.py'"]).start())
waydroidRepairUnshowMouse = configMenu.addMenu("修复 Waydroid 多窗口在部分桌面环境无法显示鼠标的问题")
waydroidRepairUnshowMouseTips = QtWidgets.QAction("此功能默认关闭（如果能正常显示鼠标指针请别开启该功能）")
waydroidRepairUnshowMouseOn = QtWidgets.QAction("开启")
waydroidRepairUnshowMouseOff = QtWidgets.QAction("关闭")
waydroidRepairUnshowMouseOn.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/SystemConfigs/Show-cursor.py'"]).start())
waydroidRepairUnshowMouseOff.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/Off-function/Off-cursor.py'"]).start())
waydroidRepairUnshowMouseTips.setDisabled(True)
waydroidRepairUnshowMouse.addAction(waydroidRepairUnshowMouseTips)
waydroidRepairUnshowMouse.addSeparator()
waydroidRepairUnshowMouse.addAction(waydroidRepairUnshowMouseOn)
waydroidRepairUnshowMouse.addAction(waydroidRepairUnshowMouseOff)
configMenu.addSeparator()
configMenu.addAction(waydroidAppListShow)
quicklyOpen = configMenu.addMenu("应用快捷打开")
waydroidSetting = QtWidgets.QAction("Waydroid 设置")
waydroidFileManager = QtWidgets.QAction("Waydroid 文件")
waydroidBrowser = QtWidgets.QAction("Waydroid 浏览器")
waydroidSetting.triggered.connect(lambda: os.system("waydroid app launch com.android.settings"))
waydroidFileManager.triggered.connect(lambda: os.system("waydroid app launch com.android.documentsui"))
waydroidBrowser.triggered.connect(lambda: os.system("waydroid app launch org.lineageos.jelly"))
quicklyOpen.addAction(waydroidSetting)
quicklyOpen.addAction(waydroidFileManager)
quicklyOpen.addAction(waydroidBrowser)
configMenu.addSeparator()
waydroidContainer = configMenu.addMenu("Waydroid 容器控制")
waydroidContainerStart = QtWidgets.QAction("开启")
waydroidContainerStop = QtWidgets.QAction("关闭")
waydroidContainerRestart = QtWidgets.QAction("重新启动")
waydroidContainerFreeze = QtWidgets.QAction("Freeze")
waydroidContainerUnfreeze = QtWidgets.QAction("Unfreeze")
waydroidContainer.addAction(waydroidContainerStart)
waydroidContainer.addAction(waydroidContainerStop)
waydroidContainer.addAction(waydroidContainerRestart)
waydroidContainer.addAction(waydroidContainerFreeze)
waydroidContainer.addAction(waydroidContainerUnfreeze)
configMenu.addAction(waydroidUpgradImage)
configMenu.addSeparator()
configMenu.addAction(waydroidShell)
downloadImageCN.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"bash '{programPath}/Runner_tools/Waydroid_Image_Installer/Install.sh'"]).start())
libhoudiniInstall.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"bash '{programPath}/Runner_tools/Libhoudini_installer/Install.sh'"]).start())
magiskInstall.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/Magisk_Installer/Magisk.py'"]).start())
widevineInstall.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"bash '{programPath}/Runner_tools/Widevine_Installer/Install.sh'"]).start())
waydroidLaguage.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"pkexec python3 '{programPath}/Runner_tools/SystemConfigs/Language.py'"]).start())
#doNotRotate.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/SystemConfigs/Do-not-rotate.py'"]).start())
multiWindowsSetOn.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/SystemConfigs/Multi_windows.py'"]).start())
multiWindowsSetOff.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"python3 '{programPath}/Runner_tools/Off-function/Off-windows-mode.py'"]).start())
waydroidAppListShow.triggered.connect(lambda: QtWidgets.QInputDialog.getMultiLineText(mainwindow, "应用列表", "", subprocess.getoutput("waydroid app list")))
waydroidUpgradImage.triggered.connect(lambda: threading.Thread(target=RunBash, args=[f"pkexec waydroid upgrade"]).start())
waydroidShell.triggered.connect(lambda: threading.Thread(target=OpenTerminal, args=[f"pkexec waydroid shell"]).start())
waydroidContainerStart.triggered.connect(lambda: threading.Thread(target=os.system, args=["pkexec waydroid container start"]).start())
waydroidContainerStop.triggered.connect(lambda: threading.Thread(target=os.system, args=["pkexec waydroid container stop"]).start())
waydroidContainerRestart.triggered.connect(lambda: threading.Thread(target=os.system, args=["pkexec waydroid container restart"]).start())
waydroidContainerFreeze.triggered.connect(lambda: threading.Thread(target=os.system, args=["pkexec waydroid container freeze"]).start())
waydroidContainerUnfreeze.triggered.connect(lambda: threading.Thread(target=os.system, args=["pkexec waydroid container unfreeze"]).start())
# 帮助 栏
helpAction = QtWidgets.QAction("程序帮助")
uploadBugAction = QtWidgets.QAction("问题反馈")
updateProgram = QtWidgets.QAction("更新程序")
programWebsite = QtWidgets.QAction("程序地址")
aboutThisProgramAction = QtWidgets.QAction("关于本程序(&A)")
helpAction.triggered.connect(showhelp)
programWebsite.triggered.connect(lambda: webbrowser.open_new_tab("https://gitee.com/gfdgd-xi/waydroid-runner"))
updateProgram.triggered.connect(UpdateWindow.ShowWindow)
uploadBugAction.triggered.connect(lambda: threading.Thread(target=os.system, args=[f"python3 '{programPath}/waydroid-runner-update-bug'"]).start())
aboutThisProgramAction.triggered.connect(showhelp)
helpMenu.addAction(helpAction)
helpMenu.addAction(uploadBugAction)
helpMenu.addSeparator()
helpMenu.addAction(programWebsite)
helpMenu.addSeparator()
helpMenu.addAction(updateProgram)
helpMenu.addAction(aboutThisProgramAction)

## 窗口属性
mainwindow.setWindowIcon(QtGui.QIcon(iconPath))

mainwindow.show()
mainwindow.resize(int(mainwindow.frameGeometry().width() * 1.8), int(mainwindow.frameGeometry().height()))

# 加载设置
apkPath.addItems(findApkHistory)
apkPath.setCurrentText("")
# 检测 Waydroid 是否存在
if os.system("which waydroid"):
    waydroidStatus.setText("Waydroid：未安装")
#os.system(f"ls {programPath}/Runner_tools/Checks/HoudiniCheck.py")
print(os.system(f"python3 '{programPath}/Runner_tools/Checks/HoudiniCheck.py'"))
libkoudiniInstallStatus.setText("Libhoudini：" + ["已安装", "未安装"][os.system(f"python3 '{programPath}/Runner_tools/Checks/HoudiniCheck.py'")>>8])
libhoudiniInstall.setEnabled(os.system(f"python3 '{programPath}/Runner_tools/Checks/HoudiniCheck.py'")>>8)
magiskInstall.setEnabled(os.system(f"python3 '{programPath}/Runner_tools/Checks/MagiskCheck.py'")>>8)
widevineInstall.setEnabled(os.system(f"python3 '{programPath}/Runner_tools/Checks/Widevine-Check.py'")>>8)
lsPosedInstallStatus.setText("LSPosed：" + ["已安装", "未安装"][os.system(f"python3 '{programPath}/Runner_tools/Checks/LSPCheck.py'")>>8])
magiskDeltaInstallStatus.setText("Magisk Delta：" + ["已安装", "未安装"][os.system(f"python3 '{programPath}/Runner_tools/Checks/MagiskCheck.py'")>>8])
wideVineInstallStatus.setText("Widevine：" + ["已安装", "未安装"][os.system(f"python3 '{programPath}/Runner_tools/Checks/Widevine-Check.py'")>>8])
# 读参数
try:
    apkPath.setCurrentText(sys.argv[1])
except:
    pass


sys.exit(app.exec_())

clean:
	python3 RemovePycacheFile.py

build:
	echo 别云间
	echo 三年羁旅客，今日又南冠。
	echo 无限山河泪，谁言天地宽。
	echo 已知泉路近，欲别故乡难。
	echo 毅魄归来日，灵旗空际看。 
	echo
	echo 译文：三年为抗清兵东走西飘荡，今天兵败被俘作囚入牢房。无限美好河山失陷伤痛泪，谁还敢说天庭宽阔地又广。已经知道黄泉之路相逼近，想到永别故乡实在心犯难。鬼雄魂魄等到归来那一日，灵旗下面要将故乡河山看。
	echo "Build DEB..."
	cp -rv information.json                     deb/opt/apps/spark-waydroid-runner/files/
	cp -rv mainwindow.py                        deb/opt/apps/spark-waydroid-runner/files/waydroid-runner
	cp -rv Language.json                        deb/opt/apps/spark-waydroid-runner/files/
	cp -rv waydroid-runner-update-bug            deb/opt/apps/spark-waydroid-runner/files/
	cp -rv launch.sh                            deb/opt/apps/spark-waydroid-runner/files/
	cp -rv LICENSE                              deb/opt/apps/spark-waydroid-runner/files/
	cp -rv defult.svg                           deb/opt/apps/spark-waydroid-runner/files/
	cp -rv defult.png                           deb/opt/apps/spark-waydroid-runner/files/
	cp -rv runner.svg                           deb/opt/apps/spark-waydroid-runner/files/
	cp -rv menu.svg                             deb/opt/apps/spark-waydroid-runner/files/
	cp -rv icon.png                             deb/opt/apps/spark-waydroid-runner/files/
	cp -rv getxmlimg.py                         deb/opt/apps/spark-waydroid-runner/files/
	cp -rv defult.svg                           deb/opt/apps/spark-waydroid-runner/files/
	cp -rv builer.svg                           deb/opt/apps/spark-waydroid-runner/files/
	cp -rv Download.py                          deb/opt/apps/spark-waydroid-runner/files/
	cp -rv updatekiller.py                      deb/opt/apps/spark-waydroid-runner/files/
	#cp -rv pkexec/*                             deb/usr/share/polkit-1/actions
	cp -rv AutoShell                            deb/opt/apps/spark-waydroid-runner/files/
	cp -rv AutoConfig.py                        deb/opt/apps/spark-waydroid-runner/files/
	cp -rv Model                                deb/opt/apps/spark-waydroid-runner/files/
	cp -rv UI                                   deb/opt/apps/spark-waydroid-runner/files/
	cp -rv ConfigLanguareRunner-help.json       deb/opt/apps/spark-waydroid-runner/files/
	cp -rv ConfigLanguareRunner.py              deb/opt/apps/spark-waydroid-runner/files/
	cp -rv ProgramFen.py                        deb/opt/apps/spark-waydroid-runner/files/
	cp -rv BuildDesktop.py                      deb/opt/apps/spark-waydroid-runner/files/
	cp -rv Runner_tools                      deb/opt/apps/spark-waydroid-runner/files/
	cp -rv Icon                                 deb/opt/apps/spark-waydroid-runner/files/
	#cp -rv pkexec                               deb/opt/apps/spark-waydroid-runner/files/
	rm -rfv deb/opt/apps/spark-waydroid-runner/files/Help/information
	python3 UpdateTime.py
	python3 RemovePycacheFile.py                #deb/opt/apps/spark-waydroid-runner/files/
	cp -rv deb /tmp/waydroid-runner-builder
	sudo chown -R root:root /tmp/waydroid-runner-builder
	sudo dpkg-deb -Z xz -b /tmp/waydroid-runner-builder spark-waydroid-runner.deb
	sudo rm -rfv /tmp/waydroid-runner-builder

install:
	make build	
	echo "Install..."
	sudo apt update
	#sudo dpkg -i spark-waydroid-runner.deb | true
	#sudo apt install -f
	sudo apt reinstall ./spark-waydroid-runner.deb
	sudo rm spark-waydroid-runner.deb

depend:
	sudo apt install python3 python3-tk python3-pip aapt \
	python3-setuptools deepin-terminal curl python3-pil\
	 python3-requests adb fonts-noto-cjk python3-numpy\
	  python3-matplotlib wget inotify-tools aria2 python3-pyqt5
	python3 -m pip install --upgrade pip          --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple
	python3 -m pip install --upgrade ttkthemes    --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple
	python3 -m pip install --upgrade pyautogui    --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple
	python3 -m pip install --upgrade keyboard     --trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple

run:
	python3 mainwindow.py
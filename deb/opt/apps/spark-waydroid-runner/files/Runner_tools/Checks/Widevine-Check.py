#!/bin/env python3
#Python3 Program
#不需要以root执行!
import os
import sys
if os.path.exists('/var/lib/waydroid/overlay/vendor/etc/vintf/manifest') == True and os.path.exists('/var/lib/waydroid/overlay/vendor/lib/mediadrm') == True and os.path.exists('/var/lib/waydroid/overlay/vendor/lib64/mediadrm') == True: sys.exit(0)
else: sys.exit(1)

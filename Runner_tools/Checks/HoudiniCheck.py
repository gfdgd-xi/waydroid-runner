#!/bin/env python3
import sys
import os
if os.path.exists('/var/lib/waydroid/overlay/system/lib/libhoudini.so') == True and os.path.exists('/var/lib/waydroid/overlay/system/lib/arm') == True and os.path.exists('/var/lib/waydroid/overlay/system/lib64/arm64') == True and os.path.exists('/var/lib/waydroid/overlay/system/etc/init/init-houdini.rc') == True:
    sys.exit(0)
sys.exit(1)

import os
import sys
if os.path.exists('/var/lib/waydroid/overlay/system/etc/init/magisk.rc') == True and os.path.exists('/var/lib/waydroid/overlay/system/etc/init/magisk') == True:
    sys.exit(0)
sys.exit(1)

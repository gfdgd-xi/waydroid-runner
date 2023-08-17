import os
import sys
if os.path.exists('/var/lib/waydroid/overlay_rw/system/system/etc/init/magisk') == True:
    sys.exit(0)
sys.exit(1)

#Please running it by root!
import os
import sys
user = os.getlogin()
if os.path.exists(f'/home/{user}/.local/share/waydroid/data/adb/lspd') == True:
    sys.exit(0)
sys.exit(1)

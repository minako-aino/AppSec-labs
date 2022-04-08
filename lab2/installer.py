import os
import pyautogui
import shutil
import hashlib
from git import Repo

git_url = "https://github.com/minako-aino/AppSec-labs.git"


def get_info():
    # username
    name = os.getlogin()
    # computer name
    computer_name = os.uname()[1]
    # folder
    folder = str(os.getcwd())
    # type/subtype of keyboard
    keyboard = str(os.popen("setxkbmap -query | grep model | awk '{print $2}'").read())
    # screen width
    screen_w = str(pyautogui.size().width)
    # mem
    disk_vol = str(shutil.disk_usage("/")[0] // (2**30))

    sysinfo_hash = hashlib.md5((name + computer_name + folder + keyboard + screen_w + disk_vol).encode('utf-8')).hexdigest()
    return sysinfo_hash


path = input("Set the path of installation: ")
Repo.clone_from(git_url, path)
print("Done.")

sysinfo = get_info()
f = open('/home/' + os.getlogin() + '/lab2.txt', 'w')
f.write(sysinfo)
f.close()

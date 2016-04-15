#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import urllib
import platform
import subprocess

class EnvInfo:
    def __init__(self, type, name):
        self.os_type = type 
        self.os_name = name 
    os_type = 'unknow'
    os_name = 'unknow'
    python_ver = 'unknow'

# confirm env info
# ---------------------------------------------------
envinfo = EnvInfo('unknow', 'unknow')
platform = platform.platform()
if -1 != platform.find('Darwin'):
    envinfo.os_type = 'mac'
elif -1 != platform.find('Linux'):
    envinfo.os_type = 'linux'
    if -1 != platform.find('Kali'): 
        envinfo.os_name = 'kali'
elif -1 != platform.find('Windows'):
    envinfo.os_name = 'windows'

python_ver = sys.version.split('.')
python_ver = python_ver[0] + '.' + python_ver[1]
envinfo.python_ver = python_ver

# delete  
# ---------------------------------------------------
os.system('sudo rm -rf /opt/bin/vimstudio')
os.system('rm -rf ~/.vimstudio')

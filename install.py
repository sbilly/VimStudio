#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import platform
import subprocess
from shutil import copyfile

class OSInfo:
    def __init__(self, type, name):
        self.type = type 
        self.name = name 

    type = 'unknow'
    name = 'unknow'


osinfo = OSInfo('unknow', 'unknow')

platform = platform.platform()
if -1 != platform.find('Darwin'):
    osinfo.type = 'mac'
elif -1 != platform.find('Linux'):
    osinfo.type = 'linux'
    if -1 != platform.find('Kali'): 
        osinfo.name = 'kali'
elif -1 != platform.find('Windows'):
    osinfo.name = 'windows'

subprocess.call(["git", "submodule", 
    "update", "--init", "--recursive"])

# plugin: fcitx
# --------------------------------------------------------------
if 'mac' == osinfo.type:
    subprocess.call(["brew", "install", 
        "fcitx-remote-for-osx", 
        "--with-input-method=baidu-pinyin"])
    copyfile('.vim/bundle/fcitx.vim/so/fcitx.vim', 
            '.vim/plugin/fcitx.vim')
elif 'linux' == osinfo.type: 
    if 'kali' == osinfo.name: 
        subprocess.call(["apt-get", "install", 
            "fcitx", "fcitx-sunpinyin", 
            "fcitx-libpinyin"])
        

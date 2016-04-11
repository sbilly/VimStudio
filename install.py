#!/usr/bin/env python
# -*- coding: utf-8 -*-
import git
import os
import subprocess
import platform
from shutil import copyfile

osinfo = {'type':'unknow', 'release':'unknow'}
platform = platform.platform()
if -1 != platform.find('Darwin'):
    osinfo['type'] = 'mac'
elif -1 != platform.find('Linux'):
    osinfo['type'] = 'linux'
    if -1 != platform.find('kali'): 
        osinfo['release'] = 'kali'
elif -1 != platform.find('Windows'):
    osinfo['type'] = 'windows'

subprocess.call(["git", "submodule", 
    "update", "--init", "--recursive"])

# plugin: fcitx
# --------------------------------------------------------------
if 'mac' == osinfo['type']:
    subprocess.call(["brew", "install", 
        "fcitx-remote-for-osx", 
        "--with-input-method=baidu-pinyin"])
    copyfile('bundle/fcitx.vim/so/fcitx.vim', 
            './plugin/fcitx.vim')
elif 'linux' == osinfo['type']: 
    if 'kali' == osinfo['release']: 
        subprocess.call(["apt-get", "install", 
            "fcitx", "fcitx-sunpinyin", 
            "fcitx-libpinyin"])
        

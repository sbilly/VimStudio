#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import platform
import subprocess
from shutil import copyfile

class OSInfo:
    def __init__(self, type, name):
        self.type = type 
        self.name = name 
    type = 'unknow'
    name = 'unknow'

# confirm os info
# -------------------------------------------
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

# confirm all submodules' version 
# -------------------------------------------
f = open('README.md')

submodule_ver = ''
submodule_name = ''
submodules = {}
is_get_submodule_name = False
is_get_submodule_ver  = False

content = f.read()
while 1:
    try:
        content = content.split('<a name=\"\">[', 1)[1]
    except IndexError:
        break
    if  '' == content:
        break
    submodule_name = content.split('][', 1)[0]
    submodule_ver = content.split('<sup>[', 1)[1].split('][', 1)[1].split(']</sup>', 1)[0]
    submodule_ver = content.split('[' + submodule_ver + ']:', 1)[1].split('/tag/', 1)[1].split('[', 1)[0]
    submodule_ver = submodule_ver[:-1]

'''
while 1:
    line = f.readline()
    if '' == line :
        break
    if -1 != line.find('<a name=\"\">['): 
        submodule_name = line.split('\">[')[1].split('][')[0]
        is_get_submodule_name = True
    elif -1 != line.find('<sup>['):
        submodule_ver = line.split('<sup>[')[1].split('][')[0]
        is_get_submodule_ver = True

    if is_get_submodule_name and is_get_submodule_ver:
        is_get_submodule_ver = False
        is_get_submodule_name = False
        submodules[submodule_name] = submodule_ver;
f.close()
'''

'''
# update all submodules 
# -------------------------------------------
subprocess.call(["git", "submodule", 
    "update", "--init", "--recursive"])
'''


# checkout specify version tag 
# -------------------------------------------
for name, ver in submodules.iteritems():
    predir = os.getcwd()
    dstdir = '.vim/bundle/' + name
    os.chdir(dstdir)
    subprocess.call(['git', 'checkout', ver])
    subprocess.call(['git', 'checkout', ver[1:]])
    os.chdir(predir)

# special case -> plugin: fcitx
# -------------------------------------------
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

# create .vim in user home  
# -------------------------------------------
home = os.path.expanduser('~')
newpath = home + '/.vim'
if not os.path.exists(newpath):
    os.makedirs(newpath)

# copy ...  
# -------------------------------------------
src = '.vim/bundle/'
dst = home + '/.vim/bundle/'
try:
    shutil.copytree(src, dst)
except OSError:
    None
src = '.vim/vimrc'
dst = home + '/.vim/vimrc'
try:
    shutil.copyfile(src, dst)
except OSError:
    None
src = '.vim/autoload'
dst = home + '/.vim/autoload'
try:
    shutil.copytree(src, dst)
except OSError:
    None
src = '.vim/ftplugin'
dst = home + '/.vim/ftplugin'
try:
    shutil.copytree(src, dst)
except OSError:
    None

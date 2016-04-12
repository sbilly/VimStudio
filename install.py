#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import urllib
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

# confirm all submodules, dep version 
# -------------------------------------------
f = open('README.md')

submodule_ver = ''
submodule_name = ''
submodules = {}
is_have_dep = True

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

    is_have_dep = True

    try:
        dep = content.split('=>', 1)[1].split('<a name=\"', 1)[0].split('\n', 1)[0].replace(' ', '')
    except IndexError:
        is_have_dep = False

    if is_have_dep:
        dep = dep.split(',')
        dep_ver = {}
        for d in dep:
            ver = ''
            name = d.split('[', 1)[1].split('](', 1)[0]
            anchor_name = d.split('(#', 1)[1].split(')', 1)[0]
            try:
                ver = content.split('<a name=\"' + anchor_name + '\">', 1)[1]
            except IndexError:
                continue
            ver = ver.split('<sup>[', 1)[1].split('][', 1)[0]
            dep_ver[name] = ver
    submodules[submodule_name] = {'self':submodule_ver, 'dep':dep_ver};

# update all submodules 
# -------------------------------------------
subprocess.call(["git", "submodule", 
    "update", "--init", "--recursive"])

# checkout specify version tag 
# -------------------------------------------
for name, ver in submodules.iteritems():
    predir = os.getcwd()
    dstdir = '.vim/bundle/' + name
    os.chdir(dstdir)
    subprocess.call(['git', 'checkout', ver['self']])
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

# special case -> plugin: YouCompleteMe 
# -------------------------------------------
if 'mac' == osinfo.type:
    #srcurl = ''
    #urllib.URLopener()
    None

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

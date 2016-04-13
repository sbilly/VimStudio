#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import urllib
import platform
import subprocess
from shutil import copyfile

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

# get vim, plugins, dependencies ver from README.md 
# ---------------------------------------------------
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

    submodule_ver = content.split('<sup>[', 1)[1].split('][', 1)[0]
    if 'master' != submodule_ver:
        submodule_ver = content.split('<sup>[', 1)[1].split('][', 1)[1].split(']</sup>', 1)[0]
        submodule_ver = content.split('[' + submodule_ver + ']:', 1)[1].split('/tag/', 1)[1].split('[', 1)[0]
        submodule_ver = submodule_ver[:-1]

    print submodule_name + ' ' + submodule_ver

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
'''
# update all submodules 
# ---------------------------------------------------
subprocess.call(["git", "submodule", 
    "update", "--init", "--recursive"])

# checkout specify tag version
# ---------------------------------------------------
for name, ver in submodules.iteritems():
    predir = os.getcwd()
    if 'vim' == name:
        dstdir = name
    else:
        dstdir = '.vim/bundle/' + name
    os.chdir(dstdir)
    subprocess.call(['git', 'checkout', ver['self']])
    os.chdir(predir)

'''

'''
# for plugin: fcitx
# ---------------------------------------------------
if 'mac' == envinfo.os_type:
    subprocess.call(["brew", "install", 
        "fcitx-remote-for-osx", 
        "--with-input-method=baidu-pinyin"])
    copyfile('.vim/bundle/fcitx.vim/so/fcitx.vim', 
            '.vim/plugin/fcitx.vim')
elif 'linux' == envinfo.os_type: 
    if 'kali' == envinfo.os_name: 
        subprocess.call(["apt-get", "install", 
            "fcitx", "fcitx-sunpinyin", 
            "fcitx-libpinyin"])

# for plugin: YouCompleteMe 
# ---------------------------------------------------
if 'mac' == envinfo.os_type:
    # dep: clang+llvm
    ver = submodules['YouCompleteMe']['dep']['LLVM'].replace('v','')
    url = 'http://llvm.org/releases/' + ver + '/'
    filename = 'clang+llvm-' + ver + '-x86_64-apple-darwin.tar.xz' 
    url += filename
    decompressdir = 'clang+llvm'
    if os.path.isfile(filename):
        subprocess.call(['rm', '-f', filename]
    subprocess.call(['wget', url])
    subprocess.call(['mkdir', decompressdir])

    subprocess.call(['tar', 'xfv', filename, 
        '-C', './' + decompressdir, '--strip-components=1'])
    subprocess.call(['rm', '-f', filename])

    subprocess.call(['mkdir', 'ycm_build'])
    predir = os.getcwd()
    dstdir = './ycm_build' 
    os.chdir(dstdir)
    
    # TODO: get vim use python version.
    python = '/usr/bin/python2.7' 
    subprocess.call(['cmake', '-G', 'Unix Makefiles', 
        '-DPATH_TO_LLVM_ROOT=../' + decompressdir, 
        '-DPYTHON_EXECUTABLE=' + python, '.', 
        '../.vim/bundle/YouCompleteMe/third_party/ycmd/cpp'])
    subprocess.call(['make']) 
    os.chdir(predir)

# create .vim in user home  
# ---------------------------------------------------
home = os.path.expanduser('~')
newpath = home + '/.vim'
if not os.path.exists(newpath):
    os.makedirs(newpath)

# copy ...  
# ---------------------------------------------------
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
'''

# compile install vim 
# ---------------------------------------------------
# chage default config file search path
filepath = './vim/src/feature.h' 
insert_content = '#define USR_VIMRC_FILE \"~/.vimstudio/.vimrc\"'
insert_line = 896
f = open(filepath, 'r')
content = f.readlines()
f.close()
tmp = "".join(content)
if -1 == tmp.find(insert_content):
    content.insert(insert_line, insert_content)
    f = open(filepath, 'w')
    content = "".join(content)
    f.write(content)
    f.close()

# TODO
# about vimgdb

# config, make, make install
predir = os.getcwd()
dstdir = 'vim'
os.chdir(dstdir)
command = ['./configure', 
    '--with-vim-name=vimstudio',
    '--with-features=huge', 
    '--enable-pythoninterp',
    '--enable-rubyinterp',
    '--enable-luainterp',
    '--enable-perlinterp',
    '--enable-cscope',
    '--with-python-config-dir=/usr/lib/python' 
        + envinfo.python_ver + '/config/',
    ]
if 'linux' == envinfo.os_type:
    command.append('--enable-gui=gtk2')
subprocess.call(command)
subprocess.call(['make', 'clean']) 
subprocess.call(['make']) 
subprocess.call(['make', 'install']) 
os.chdir(predir)

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
    v = ver['self']
    os.chdir(dstdir)
    subprocess.call(['git', 'checkout', '.'])
    subprocess.call(['git', 'checkout', 'master'])
    subprocess.call(['git', 'clean', '-fd'])
    subprocess.call(['git', 'checkout', v])
    os.chdir(predir)

home = os.path.expanduser('~')

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

'''
# for plugin: YouCompleteMe 
# ---------------------------------------------------
# dep: clang+llvm
ver = submodules['YouCompleteMe']['dep']['LLVM'].replace('v','')
url = 'http://llvm.org/releases/' + ver + '/'
filename = 'clang+llvm-' + ver 
if 'mac' == envinfo.os_type:
    filename += '-x86_64-apple-darwin.tar.xz' 
elif 'linux' == envinfo.os_type:
    if 'kali' == envinfo.os_name:
        filename += '-x86_64-linux-gnu-debian8.tar.xz' 
url += filename
decompressdir = 'clang+llvm'
if os.path.isfile(filename):
    subprocess.call(['rm', '-f', filename])

subprocess.call(['wget', url])
subprocess.call(['mkdir', decompressdir])

subprocess.call(['tar', 'xfv', filename, 
    '-C', './' + decompressdir, '--strip-components=1'])
subprocess.call(['rm', '-f', filename])

subprocess.call(['mkdir', 'ycm_build'])
predir = os.getcwd()
dstdir = './ycm_build' 
os.chdir(dstdir)

python = '/usr/bin/python' + envinfo.python_ver  
subprocess.call(['cmake', '-G', 'Unix Makefiles', 
    '-DPATH_TO_LLVM_ROOT=../' + decompressdir, 
    '-DPYTHON_EXECUTABLE=' + python, '.', 
    '../.vim/bundle/YouCompleteMe/third_party/ycmd/cpp'])
subprocess.call(['make', 'ycm_core']) 
os.chdir(predir)

'''

# create .vimstudio in user home  
# ---------------------------------------------------
newpath = home + '/.vimstudio/.vim/bundle'
if not os.path.exists(newpath):
    subprocess.call(['mkdir', '-p', newpath]) 

# copy ...  
# ---------------------------------------------------
dst = home + '/.vimstudio/'
src = './.vimrc'
subprocess.call(['cp', src, dst])
dst = home + '/.vimstudio/.vim/'
src = './.vim/autoload'
subprocess.call(['cp', '-r', src, dst])
src = './.vim/ftplugin'
subprocess.call(['cp', '-r', src, dst])
src = './.vim/plugin'
subprocess.call(['cp', '-r', src, dst])
src = './.vim/vimrc'
subprocess.call(['cp', src, dst])
dst = home + '/.vimstudio/.vim/'
src = './.vim/doc'
subprocess.call(['cp', '-r', src, dst])
src = './.vim/.ycm_extra_conf.py'
subprocess.call(['cp', src, dst])
for name, ver in submodules.iteritems():
    if 'vim' == name:
        continue
    src = './.vim/bundle/' + name
    dst = home + '/.vimstudio/.vim/bundle/'
    subprocess.call(['cp', '-r', src, dst])

# compile install vim 
# ---------------------------------------------------
# chage .vimrc file default search path
filepath = './vim/src/feature.h' 
insert_content = '#define USR_VIMRC_FILE \"~/.vimstudio/.vimrc\"'
f = open(filepath, 'r')
content = f.read()
f.close()
if -1 == content.find(insert_content):
    f = open(filepath, 'w')
    content += insert_content 
    f.write(content)
    f.close()

# change .vim folder default search path 
# unix os, os_unix.h include macos
filepath = './vim/src/os_unix.h' 
f = open(filepath, 'r')
content = f.readlines()
f.close()
cond1 = False
cond2 = False
cond3 = False
target_str = '~/.vim'
replace_str = '~/.vimstudio/.vim'
content_str = ''
for line in content:
    if -1 != line.find('DFLT_RUNTIMEPATH'):
        cond1 = True
    if -1 != line.find(target_str):
        cond2 = True
    if -1 == line.find(replace_str):
        cond3 = True
    if cond1 and cond2 and cond3:
        line = line.replace(target_str, replace_str)
    cond1 = False
    cond2 = False
    cond3 = False
    line_str = "".join(line)
    content_str = content_str + line_str
f = open(filepath, 'w')
f.write(content_str)
f.close()

# change os_unix.c for bug
if 'mac' == envinfo.os_type:
    filepath = './vim/src/os_unix.c' 
    f = open(filepath, 'r')
    content = f.readlines()
    target_str = 'const struct sigaltstack *ss, struct sigaltstack *oss'
    replace_str = 'const stack_t *restrict ss, stack_t *restrict oss'
    content_str = ''
    cond = False
    for line in content:
        if -1 != line.find(target_str):
            cond = True
        if cond:
            line = line.replace(target_str, replace_str)
        cond = False
        line_str = "".join(line)
        content_str = content_str + line_str
    f = open(filepath, 'w')
    f.write(content_str)
    f.close()

# config, make, make install
predir = os.getcwd()
dstdir = 'vim'
os.chdir(dstdir)

command = ['make', 'distclean']
subprocess.call(command)

command = ['./configure', 
    '--prefix=/usr/local/bin',
    '--with-vim-name=vimstudio',
    '--with-features=huge', 
    '--enable-pythoninterp',
    '--enable-gdb',
    #'--enable-rubyinterp',
    #'--enable-luainterp',
    #'--enable-perlinterp',
    '--enable-gui=auto',
    '--enable-cscope',
    '--with-python-config-dir=/usr/lib/python' 
        + envinfo.python_ver + '/config/',
    ]
if 'mac' == envinfo.os_type:
    # command.append('--enable-gui=athena')
    # command.append('--disable-darwin')
    None

if 'linux' == envinfo.os_type:
    None

subprocess.call(command)
subprocess.call(['make', 'clean']) 
subprocess.call(['make']) 
#subprocess.call(['clear']) 
subprocess.call(['sudo', 'make', 'install']) 
#subprocess.call(['clear']) 
os.chdir(predir)

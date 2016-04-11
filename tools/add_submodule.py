#!/usr/bin/env python
#-*- coding: utf-8 -*-
f = open('../.gitmodules')
#for line in f:
#    if -1 != line.find('[submodule'):
import subprocess

url = ''
dstpath = ''
is_get_url = False
is_get_path = False

while 1:
    line = f.readline()
    if '' == line:
        break
    
    if -1 != line.find('[submodule'): 
        dstpath = line.split('submodule \"')[1].split('\"')[0]
        is_get_path = True
        line = f.readline()
    elif -1 != line.find('url'):
        url = line.split('=')[1][:-1].strip()
        is_get_url = True

    if is_get_url and is_get_path:
        is_get_url = False
        is_get_path = False
        subprocess.call(['git', 'submodule', 'add', url, dstpath])
f.close()

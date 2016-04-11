#!/usr/bin/env python
# -*- coding: utf-8 -*-
import git
import os
import subprocess
from shutil import copyfile

# git.Git().clone("https://github.com/Rykka/clickable.vim")

subprocess.call(["git", "submodule", "update", "--init", "--recursive"])

print "hello"


copyfile('bundle/fcitx.vim/so/fcitx.vim', './plugin/fcitx.vim')



#!/usr/bin/env python
# -*- coding: utf-8 -*-
import git
import os
from shutil import copyfile

# git.Git().clone("https://github.com/Rykka/clickable.vim")

copyfile('bundle/fcitx.vim/so/fcitx.vim', './plugin/fcitx.vim')



# coding=utf-8
import sys
import os

__author__ = 'Sapocaly'


def configure_dir():
    # 增加package路径
    sys.path.append(os.path.abspath('..'))
    # 更改工作路径
    os.chdir('..')

configure_dir()
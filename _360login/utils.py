# coding=utf-8
"""
@author: comwrg
@license: MIT
@time : 2017/08/14 15:48
@desc : Some utils for 360 api.
"""

import hashlib


def md5(s):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()
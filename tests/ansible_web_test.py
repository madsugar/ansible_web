#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:54
# @Author  : Administrator
# @Site    : 
# @File    : ansible_web_test.py
# @Software: PyCharm
import requests

data = {'hosts': ['192.168.1.30'], 'username': 'liuxin', 'passwd': '1234567', 'module_name': 'shell',
        'module_args': 'whoami'}

# a = requests.get("http://192.168.1.30:80/api_1_0/test_api", params=data).json()
a = requests.post("http://192.168.1.30:80/api_1_0/test_api", data=data).json()
print(a)
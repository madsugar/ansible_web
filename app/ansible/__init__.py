#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 16:20
# @Author  : Administrator
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm

from app.ansible.models import AnsibleRunner, CallbackBase


def create_ansible():
    return AnsibleRunner(remote_user='liuxin', conn_pass='1234567', group=['192.168.1.30'], module_name='shell',
                         module_args='whoami')

if __name__ == '__main__':
    a = create_ansible()
    print(a.order_run())

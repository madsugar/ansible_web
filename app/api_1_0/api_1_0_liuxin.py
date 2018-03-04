#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : Administrator
# @Site    : 
# @File    : api_1_0_liuxin.py
# @Software: PyCharm

from ..api_1_0 import api_1_0
from flask_restful import Api, Resource
from ..ansible.models import AnsibleRunner
from flask import request, jsonify

my_api = Api(api_1_0)


class HelloWorld(Resource):
    def get(self):
        return jsonify({'hello': 'world'})


class AnsibleRunnerApi(Resource):
    def post(self):
        hosts = request.form.getlist('hosts')
        # hosts = request.form.get('hosts')
        username = request.form['username']
        passwd = request.form['passwd']
        module_name = request.form['module_name']
        module_args = request.form['module_args']
        print(hosts, username, passwd, module_name, module_args)
        a = AnsibleRunner(remote_user=username, conn_pass=passwd, group=hosts, module_name=module_name,
                          module_args=module_args)
        res = a.order_run()
        print(res)
        return jsonify(res)


my_api.add_resource(HelloWorld, '/test_hello', endpoint='test_hello')
my_api.add_resource(AnsibleRunnerApi, '/test_api', endpoint='test_api')

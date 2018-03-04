#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : Administrator
# @Site    : 
# @File    : api_1_0_1.py
# @Software: PyCharm

from ..api_1_0 import api_1_0
from flask_restful import Api, Resource
from ..ansible.models import AnsibleRunner
from flask import request, jsonify

my_api = Api(api_1_0)


class HelloWorld(Resource):
    def get(self):
        return jsonify({'hello': 'world'})

my_api.add_resource(HelloWorld, '/test_hello', endpoint='test_hello')

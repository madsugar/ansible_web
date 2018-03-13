#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/8 21:11
# @Author  : Administrator
# @Site    : 
# @File    : ansible_models.py
# @Software: PyCharm

import json, os
from collections import namedtuple
# from ansible.executor.task_result import TaskResult
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.playbook import Playbook, Play, playbook_include

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class ResultCallback(CallbackBase):
    def __init__(self):
        self.x = dict()
        self.y = dict()
        self.z = dict()

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        # 执行成功后的结果放到x字典中
        self.x[host.name] = result._result['stdout']
        # print(self.x)

    def v2_runner_on_failed(self, result, ignore_errors=True):
        host = result._host
        # 执行后的结果放到x失y字典中
        self.y[host.name] = result._result['stderr_lines']

    def v2_runner_on_unreachable(self, result):
        host = result._host
        # 后的网络不结果放到x通z字典中
        self.z[host.name] = result._result['msg']

    def v2_playbook_on_play_start(self, play):
        name = play.get_name().strip()
        if not name:
            msg = "PLAY"
        else:
            msg = "PLAY {}".format(name)
        print(msg)

    # def v2_playbook_on_stats(self, stats):
    #     hosts = sorted(stats.processed.keys())
    #     for h in hosts:
    #         t = stats.summarize(h)
    #         msg = "PLAY RECAP [%s] : %s %s %s %s %s" % (
    #             h,
    #             "ok: %s" % (t['ok']),
    #             "changed: %s" % (t['changed']),
    #             "unreachable: %s" % (t['unreachable']),
    #             "skipped: %s" % (t['skipped']),
    #             "failed: %s" % (t['failures']),
    #         )
    #     print(msg)


class AnsibleRunner:
    def __init__(self, remote_user='liuxin', conn_pass='1234567', hosts='{}/hosts'.format(BASE_DIR),
                 play_source=['{}/playbook'.format(BASE_DIR)]):
        # 在remote服务器上执行命令的用户
        self.remote_user = remote_user
        # 执行命令用户的密码
        self.conn_pass = conn_pass
        # 设置所有主机列表
        self.hosts = hosts
        # 设置playbook的入口
        self.play_source = play_source

        self.Options = namedtuple('Options',
                                  ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user',
                                   'remote_user', 'check', 'diff'])
        # initialize needed objects
        self.loader = DataLoader()
        self.options = self.Options(connection='smart', module_path=None, forks=100, become=None, become_method=None,
                                    become_user=None, remote_user=self.remote_user, check=False, diff=False)
        self.passwords = dict(vault_pass='secret', conn_pass=self.conn_pass)
        # Instantiate our ResultCallback for handling results as they come in
        self.results_callback = ResultCallback()

        self.inventory = InventoryManager(loader=self.loader, sources=[self.hosts])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def order_run(self, group='test01', module_name='shell', module_args='hostname'):
        # create play with tasks
        play_source = dict(
            name="Ansible {} {}".format(module_name, module_args),
            hosts=group,
            gather_facts='no',
            tasks=[
                dict(action=dict(module=module_name, args=module_args), register='shell_out'),
                # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
            ]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                # stdout_callback=self.results_callback,
                # Use our custom callback instead of the ``default`` callback plugin
            )
            result = tqm.run(play)
            # print(result)
        finally:
            if tqm is not None:
                tqm.cleanup()
            # return result
            # 这里可以再进一步改进的，实现实时的现实执行结果
            # return [self.results_callback.x, self.results_callback.y, self.results_callback.z]

    def playbook_run(self, group='test01', roles=['test01']):
        # create play with tasks
        play_source = dict(
            name="Ansible Playbook {}".format(roles),
            hosts=group,
            gather_facts='no',
            roles=roles
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                # stdout_callback=self.results_callback,
                # Use our custom callback instead of the ``default`` callback plugin
            )
            result = tqm.run(play)
            # print(result)
        finally:
            if tqm is not None:
                tqm.cleanup()
            # return result
            # 这里可以再进一步改进的，实现实时的现实执行结果
            # return [self.results_callback.x, self.results_callback.y, self.results_callback.z]

a = AnsibleRunner(remote_user='root', conn_pass='123456')
res = a.order_run(group=['192.168.1.30'], module_args='hostname')
# # res = a.playbook_run(group='test01', roles=['test02'])
print(res)

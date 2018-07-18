#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
#
# Authors: Tianjun <ibumblebeet@gmail.com>
# GitHub:
# Purpose: Delete the log file for the specified directory.
"""

from pyharbor.harborclient import HarborClient
import sys

host = "dockerhub.eaxmple.cn"
user = "tianjun"
password = "123abcABC"


def change_list(tag_list):
    new_list = []
    for num in tag_list:
        new_list.append(int(num))
    new_list.sort()
    return new_list


def delete_repo(project_name):
    project_info = dict()
    client = HarborClient(host, user, password)
    client.login()
    result_projects = client.get_projects()
    for project in result_projects:
        project_info[project['name']] = project['project_id']
    if project_name in project_info.keys():
        handler_unit(harbor_client=client, project_id=project_info[project_name])
    elif project_name == 'all':
        for project_name in project_info.keys():
            handler_unit(harbor_client=client, project_id=project_info[project_name])
    else:
        print('"%s" project name not exist' % project_name)


def handler_unit(harbor_client, project_id):
    res_repo = harbor_client.get_repositories(project_id)
    for simple_repo in res_repo:
        tag_repo = harbor_client.get_repository_tags(simple_repo)
        if 5 < tag_repo.__len__() and 'latest' not in tag_repo:
            res_list = change_list(tag_repo)
            for tag_history in res_list[0:-5]:
                res = harbor_client.delete_tag_of_repository(simple_repo, tag_history)
                print("deleted successfully %s:%s  result: %s" % (simple_repo, tag_history, res))
        elif 5 < tag_repo.__len__() and 'latest' in tag_repo:
            tag_repo.remove('latest')
            res_list = change_list(tag_repo)
            for tag_history in res_list[0:-5]:
                res = harbor_client.delete_tag_of_repository(simple_repo, tag_history)
                print("deleted successfully %s:%s  result: %s" % (simple_repo, tag_history, res))
        else:
            pass


if __name__ == '__main__':
    """
    该脚本根据输入的项目名称，清除对应项目下的docker镜像，默认只保留5个最新的镜像。以tag number排序。
    带有latest标签会保留6个，其中一个是latest，其余5个为历史镜像。
    使用方法：python 文件名 'project_name1' 'project_name2' 'project_name3' ....,,
    注意，可以使用 'all' 参数清理对应账号下对应所有项目。该操作注意使用，一般由管理员操作。
    """
    try:
        for projected_name in sys.argv[1:]:
            delete_repo(project_name=projected_name)
    except SyntaxError as e:
        print('parameter error: %s' % e)


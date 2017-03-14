import requests
import json
from rally_api.information import *
from mysql_tools.mysql_curd import *


class Persistable(object):
    def __init__(self, object_id):
        self.id = object_id
        self.classname = self.__class__.__name__
        self.url = 'https://rally1.rallydev.com/slm/webservice/v2.0/{0}/{1}'.format(self.classname, self.id)
        # self.sub_url = 'https://rally1.rallydev.com/slm/webservice/v2.0/{0}' + '?{1}=' + self.url + '&query=' \
        #                '&fetch=true&start=1&pagesize=2000'
        self.sub_url = self.url + '{0}?start={1}&pagesize=2000&fetch=1'

    def get_information(self):
        self.information = requests.get(self.url, headers=headers).text
        return self.information

    def create_mysql_param(self):
        param = {}
        self.get_information()
        print(self.information)
        data = json.loads(self.information)[self.classname]
        for _ in data.keys():
            value = data.get(_)
            if not _ == 'Errors' and not _ == 'Warnings':
                if value is None:
                    value = ''
                if isinstance(value, dict):
                    try:
                        sub_value = value['_refObjectUUID'].split('/')[-1]
                        param[_ + '/' + value['_type']] = sub_value
                        continue
                    except IndexError and KeyError:
                        continue
                param[_] = value
        return param

    def insert_mysql_param(self):
        param = {}
        self.get_information()
        print(self.information)
        data = json.loads(self.information)[self.classname]
        for _ in data.keys():
            value = data.get(_)
            if not _ == 'Errors' and not _ == 'Warnings':
                if value is None:
                    continue
                if isinstance(value, dict):
                    try:
                        sub_value = value['_refObjectUUID'].split('/')[-1]
                        param[_ + '/' + value['_type']] = sub_value
                        continue
                    except IndexError and KeyError:
                        continue
                param[_] = value
        return param

    def get_sub_id(self, sub):
        sub_id = []
        result = requests.get(self.sub_url.format(sub, 1), headers=headers).text
        data = json.loads(result)
        for _ in data['QueryResult']['Results']:
            sub_id.append(_['_ref'].split('/')[-1])
        object_num = data['QueryResult']['TotalResultCount']
        if object_num > 2000:
            for _ in (2000, object_num, 2000):
                result = requests.get(self.sub_url.format(sub, _), headers=headers).text
                temp_data = json.loads(result)
                temp_data = temp_data['QueryResult']['Results']
                for temp in temp_data:
                    sub_id.append(temp['_ref'].split('/')[-1])
        return sub_id


class Subscription(Persistable):

    def __init__(self, object_id=119795615):
        super(Subscription, self).__init__(object_id)

    def get_workspace_id(self):
        return super(Subscription, self).get_sub_id('/Workspaces')


class Workspace(Persistable):
    def __init__(self, object_id):
        super(Workspace, self).__init__(object_id)

    def get_project_id(self):
        return super(Workspace, self).get_sub_id('/projects')


class Project(Persistable):

    def __init__(self, object_id):
        super(Project, self).__init__(object_id)

    def get_release_id(self):
        return super(Project, self).get_sub_id('/releases')

    def get_iteration_id(self):
        return super(Project, self).get_sub_id('/iterations')

    def get_teammembers_id(self):
        """
        :return:[user_id]
        """
        return super(Project, self).get_sub_id('/teammembers')


class Release(Persistable):

    def __init__(self, object_id):
        super(Release, self).__init__(object_id)


class Iteration(Persistable):

    def __init__(self, object_id):
        super(Iteration, self).__init__(object_id)


class PortfolioItem(Persistable):
    """
    feature theme initiative
    """
    pass


class Feature(Persistable):
    pass


class Theme(Persistable):
    pass


class Initiative(Persistable):
    pass


def get_portfolioitem_id(name=''):
    """
    默认获得portfolioitem传参获得feature
    :param name:
    :return:
    """
    sub_id = []
    result = requests.get(portfolioitem_ids_url.format(name,1), headers=headers).text
    data = json.loads(result)
    for _ in data['QueryResult']['Results']:
        sub_id.append(_['_ref'].split('/')[-1])
    object_num = data['QueryResult']['TotalResultCount']
    if object_num > 2000:
        for _ in (2000, object_num, 2000):
            result = requests.get(portfolioitem_ids_url.format(name, _),
                                  headers=headers).text
            temp_data = json.loads(result)
            temp_data = temp_data['QueryResult']['Results']
            for temp in temp_data:
                sub_id.append(temp['_ref'].split('/')[-1])
    return sub_id


if __name__ == '__main__':
    print(get_portfolioitem_id('feature'))

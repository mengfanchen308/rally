import requests
import json
from rally_api.information import *
import datetime


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
    def __init__(self, object_id):
        super(Feature, self).__init__(object_id)
        self.url = 'https://rally1.rallydev.com/slm/webservice/v2.0/PortfolioItem/{0}/{1}'\
            .format(self.classname, self.id)


class Theme(Persistable):

    def __init__(self, object_id):
        super(Theme, self).__init__(object_id)
        self.url = 'https://rally1.rallydev.com/slm/webservice/v2.0/PortfolioItem/{0}/{1}'.format(self.classname,
                                                                                                  self.id)


class Initiative(Persistable):
    def __init__(self, object_id):
        super(Initiative, self).__init__(object_id)
        self.url = 'https://rally1.rallydev.com/slm/webservice/v2.0/PortfolioItem/{0}/{1}'\
            .format(self.classname, self.id)


class HierarchicalRequirement(Persistable):

    def get_task_id(self):
        return super(HierarchicalRequirement, self).get_sub_id('/tasks')

class Task(Persistable):
    pass



def get_object_id(url):
    """
    hierarchicalrequirement,task, feature,theme,initiave,portfolioitem,project,workspath,subscription
    :param url:
    :return:
    """
    sub_id = []
    result = requests.get(url + '?start={0}&pagesize=2000&fetch=1'.format(1), headers=headers).text
    data = json.loads(result)
    for _ in data['QueryResult']['Results']:
        sub_id.append(_['_ref'].split('/')[-1])
    object_num = data['QueryResult']['TotalResultCount']
    if object_num > 2000:
        for _ in range(2001, object_num, 2000):
            result = requests.get(url + '?start={0}&pagesize=2000&fetch=1'.format(_),
                                  headers=headers).text
            temp_data = json.loads(result)
            temp_data = temp_data['QueryResult']['Results']
            for temp in temp_data:
                sub_id.append(temp['_ref'].split('/')[-1])
    return sub_id


def get_object_id_latest(url, time=2):
    """
    time时间间隔默认两天
    :param url:
    :param time:
    :return:
    """
    sub_id = []
    query_time = (datetime.datetime.now()-datetime.timedelta(days=time)).strftime('%Y-%m-%dT%H:%M:%SZ')
    result = requests.get(url + '?query=(LastUpdateDate >= "{0}")'
                                '&start={1}&pagesize=2000'
                                '&fetch=1'.format(query_time,1), headers=headers).text
    data = json.loads(result)
    for _ in data['QueryResult']['Results']:
        sub_id.append(_['_ref'].split('/')[-1])
    object_num = data['QueryResult']['TotalResultCount']
    if object_num > 2000:
        for _ in range(2001, object_num, 2000):
            result = requests.get(url + '?start={0}&pagesize=2000&fetch=1'.format(_),
                                  headers=headers).text
            temp_data = json.loads(result)
            temp_data = temp_data['QueryResult']['Results']
            for temp in temp_data:
                sub_id.append(temp['_ref'].split('/')[-1])
    return sub_id


def get_iteration_id_latest(url, time=2):
    """
    iteration条件不同需要单独
    :param url:
    :param time:
    :return:
    """
    sub_id = []
    query_time = (datetime.datetime.now() - datetime.timedelta(days=time)).strftime('%Y-%m-%dT%H:%M:%SZ')
    result = requests.get(url + '?query=(EndDate >= "{0}")'
                                '&start={1}&pagesize=2000'
                                '&fetch=1'.format(query_time, 1), headers=headers).text
    data = json.loads(result)
    for _ in data['QueryResult']['Results']:
        sub_id.append(_['_ref'].split('/')[-1])
    object_num = data['QueryResult']['TotalResultCount']
    if object_num > 2000:
        for _ in range(2001, object_num, 2000):
            result = requests.get(url + '?start={0}&pagesize=2000&fetch=1'.format(_),
                                  headers=headers).text
            temp_data = json.loads(result)
            temp_data = temp_data['QueryResult']['Results']
            for temp in temp_data:
                sub_id.append(temp['_ref'].split('/')[-1])
    return sub_id


if __name__ == '__main__':
    print(len(get_object_id(iteration_ids_url)))
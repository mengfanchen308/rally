import requests
import json
from rally_api.information import *


class Persistable(object):
    def __init__(self, object_id):
        self.id = object_id
        self.url = 'https://rally1.rallydev.com/slm/webservice/v2.0/{0}/{1}'.format(self.__class__.__name__, self.id)
        # self.sub_url = 'https://rally1.rallydev.com/slm/webservice/v2.0/{0}' + '?{1}=' + self.url + '&query=' \
        #                '&fetch=true&start=1&pagesize=2000'
        self.sub_url = self.url + '{0}?start={1}&pagesize=2000'

    def get_information(self):
        self.information = requests.get(self.url, headers=headers).text
        return self.information

    def insert_mysql(self):
        pass

    def get_sub_id(self, sub):
        sub_id = []
        result = requests.get(self.sub_url.format(sub, 1), headers=headers).text
        data = json.loads(result)
        for _ in data['QueryResult']['Results']:
            sub_id.append(_['_ref'].split('/')[-1])
        object_num = data['QueryResult']['TotalResultCount']
        if object_num > 2000:
            for _ in (2000, object, 2000):
                result = requests.get(self.sub_url.format(sub, _), headers=headers).text
                temp_data = json.loads(result)
                temp_data = temp_data['QueryResult']['Results']
                for _ in temp_data:
                    sub_id.append(_['_ref'].split('/')[-1])
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


class PortfolioItem(Persistable):
    """
    feature theme initiative
    """

    def __init__(self, object_id):
        super(PortfolioItem, self).__init__(object_id)

    def get_PortfolioItem_id(self, name=''):
        """
        默认返回所有feature,theme,initiative.传入参数即可选择
        :param name:
        :return:
        """
        return super(PortfolioItem, self).get_sub_id(name)


if __name__ == '__main__':
    pass

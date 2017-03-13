import requests
import json
from rally_api.information import *


class Persistable(object):
    def __init__(self, object_id):
        self.id = object_id
        self.url = 'https://rally1.rallydev.com/slm/webservice/v2.0/{0}/{1}'.format(self.__class__.__name__, self.id)

    def get_information(self):
        self.information = requests.get(self.url, headers=headers).text
        return self.information

    def insert_mysql(self):
        pass

    def get_sub_id(self):
        result = requests.get(self.url + '/Workspaces').text
        data = json.loads(result)['QueryResult']['Results']
        sub_id = []
        for _ in data:
            sub_id.append(_['_ref'])
        return sub_id


class Subscription(Persistable):

    def __init__(self, object_id):
        super(Subscription, self).__init__(object_id)


class Workspace(Persistable):

    def __init__(self, object_id):
        super(Workspace, self).__init__(object_id)


class PortfolioItem(Persistable):

    def __init__(self, object_id):
        super(PortfolioItem, self).__init__(object_id)


class Feature(Persistable):

    def __init__(self, object_id):
        super(Feature, self).__init__(object_id)



if __name__ == '__main__':
    print(requests.get('https://rally1.rallydev.com/slm/webservice/v2.0/portfolioItem?workspace=https://rally1.rallydev.com/slm/webservice/v2.0/workspace/2261734389&start=1&pagesize=2000', headers=headers).text)
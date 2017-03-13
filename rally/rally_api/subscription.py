import requests
import json
from rally_api.information import *


class Subscription(object):

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


class Workspace(Subscription):

    def __init__(self, object_id):
        super(Workspace, self).__init__(object_id)



if __name__ == '__main__':
    shiyan = Workspace('119795615')
    print(shiyan.get_information())
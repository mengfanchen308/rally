import requests
from rally_api.information import *
import json
def print_name(name):
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<this is {0} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'.format(name))
url = ''
page = requests.get('https://rally1.rallydev.com/slm/webservice/v2.0/subscription/119795615', headers=headers).text
print_name('Subscription')
print(page)
result = json.loads(page)['Subscription']['Workspaces']
for _ in result.keys():
    if _ == '_ref':
        url = result.get(_)
        print_name('Workspaces')
        print(url)

page = requests.get(url, headers=headers).text
print(page)
result = json.loads(page)['QueryResult']['Results'][0]
for _ in result.keys():
    if _ == '_ref':
        url = result.get(_)
        print_name('Workspace')
        print(url)

page = requests.get(url, headers=headers).text
print(page)
result = json.loads(page)['Workspace']['Projects']
for _ in result.keys():
    if _ == '_ref':
        url = result.get(_)
        print_name('Projects')
        print(url)

page = requests.get(url, headers=headers).text
print(page)
result = json.loads(page)['QueryResult']['Results']
for re in result:
    print(re['_ref'])
    page = requests.get(re['_ref'], headers=headers).text
    result = json.loads(page)


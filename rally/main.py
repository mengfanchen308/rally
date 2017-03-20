from rally_api.Items import *
from mysql_tools.mysql_curd import *
import requests

tool = MysqlCurd('rally')
tool.connect_mysql()


def initialize_create(root):
    param = root.create_mysql_param()
    tool.create_table_auto(root.__class__.__name__, param)
    tool.replace_mysql(root.__class__.__name__, param)


def initialize(root):
    try:
        param = root.insert_mysql_param()
        tool.replace_mysql(root.__class__.__name__, param)
    except KeyError and IndexError and requests.exceptions.ConnectionError \
            and TimeoutError and pymysql.err.InternalError as e:
        tool.replace_mysql('error_object', {'name': root.__class__.__name__, 'id': root.id, 'reason': repr(e)})
        return False


def initialize_mysql_table():
    root = Subscription()
    initialize_create(root)
    workspace = Workspace(root.get_workspace_id()[0])
    initialize_create(workspace)
    project = Project(workspace.get_project_id()[0])
    initialize_create(project)
    release = Release(project.get_release_id()[0])
    initialize_create(release)
    iteration = Iteration(project.get_iteration_id()[0])
    initialize_create(iteration)
    # feature = Feature(20475457565)
    # initialize_create(feature)
    # initiative = Initiative(get_object_id(initiative_ids_url)[0])
    # initialize_create(initiative)
    # theme = Theme(get_object_id(theme_ids_url)[0])
    # initialize_create(theme)
    # us = HierarchicalRequirement(91498157780)
    # initialize_create(us)
    # task = Task(91251527632)
    # initialize_create(task)

def insert_mysql_test():
    root = Subscription()
    initialize(root)
    workspace = Workspace(root.get_workspace_id()[0])
    initialize(workspace)
    for _ in workspace.get_project_id():
        project = Project(_)
        initialize(project)
        for temp in project.get_release_id():
            release = Release(temp)
            initialize(release)
        for temp in project.get_iteration_id():
            iteration = Iteration(temp)
            initialize(iteration)
    # for _ in get_object_id(feature_ids_url):
    #     feature = Feature(_)
    #     initialize(feature)
    # for _ in get_object_id(initiative_ids_url):
    #     initiative = Initiative(_)
    #     initialize(initiative)
    # for _ in get_object_id(theme_ids_url):
    #     theme = Theme(_)
    #     initialize(theme)
    # for _ in get_object_id_latest(hierarchicalrequirement_ids_url):
    #     us = HierarchicalRequirement(_)
    #     initialize(us)
    # for _ in get_object_id_latest(task_ids_url):
    #     task = Task(_)
    #     initialize(task)


def daily_job(days):
    subscription = Subscription()
    initialize(subscription)
    urls = [workspace_ids_url, project_ids_url, release_ids_url]
    for url in urls:
        for _ in get_object_id(url):
            if url == workspace_ids_url:
                temp = Workspace(_)
            elif url == project_ids_url:
                temp = Project(_)
            else:
                temp = Release(_)
            initialize(temp)

    for _ in get_iteration_id_latest(iteration_ids_url, days):
        iteration = Iteration(_)
        initialize(iteration)

    urls = [feature_ids_url, initiative_ids_url, theme_ids_url, hierarchicalrequirement_ids_url, task_ids_url]
    # 可以尝试一下python反射机制
    for url in urls:
        if url == feature_ids_url:
            for _ in get_object_id_latest(url, days):
                temp = Feature(_)
                initialize(temp)
        elif url == initiative_ids_url:
            for _ in get_object_id_latest(url, days):
                temp = Initiative(_)
                initialize(temp)
        elif url == theme_ids_url:
            for _ in get_object_id_latest(url, days):
                temp = Theme(_)
                initialize(temp)
        elif url == hierarchicalrequirement_ids_url:
            for _ in get_object_id_latest(url, days):
                temp = HierarchicalRequirement(_)
                initialize(temp)
        elif url == task_ids_url:
            for _ in get_object_id_latest(url, days):
                temp = Task(_)
                initialize(temp)
    exit(0)


def all_job():
    subscription = Subscription()
    initialize(subscription)
    urls = {'Workspace': workspace_ids_url,
            'Project': project_ids_url,
            'Release': release_ids_url,
            'Iteration': iteration_ids_url,
            'Feature': feature_ids_url,
            'Initiative': initiative_ids_url,
            'Theme': theme_ids_url,
            'HierarchicalRequirement': hierarchicalrequirement_ids_url,
            'Task': task_ids_url}
    for key in urls.keys():
        ids = get_object_id(urls.get(key))
        print(key, len(ids))
        # temp = globals()[key](ids[0])
        # initialize(temp)
        for _ in get_object_id(urls.get(key)):
            temp = globals()[key](_)
            initialize(temp)


def main():
    all_job()
    # daily_job(2)
    error = tool.query_mysql('error_object', ['name', 'id'])
    count = 0
    while len(error) != 0:
        for _ in error:
            temp = globals()[_[0]](_[1])
            # 反射机制
            initialize(temp)
            tool.delete_mysql('error_object',{'id': _[1]})
        error = tool.query_mysql('error_object', ['name', 'id'])
        count += 1
        if count >= 3:
            break
if __name__ == '__main__':
    main()
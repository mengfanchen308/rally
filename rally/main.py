from rally_api.Items import *
from mysql_tools.mysql_curd import *

tool = MysqlCurd('rally')
tool.connect_mysql()


def initialize_create(root):
    param = root.create_mysql_param()
    tool.create_table_auto(root.__class__.__name__, param)
    tool.replace_mysql(root.__class__.__name__, param)


def initialize(root):
    param = root.insert_mysql_param()
    tool.replace_mysql(root.__class__.__name__, param)


def initialize_mysql_table():
    # root = Subscription()
    # initialize_create(root)
    # workspace = Workspace(root.get_workspace_id()[0])
    # initialize_create(workspace)
    # project = Project(workspace.get_project_id()[0])
    # initialize_create(project)
    # release = Release(project.get_release_id()[0])
    # initialize_create(release)
    # iteration = Iteration(project.get_iteration_id()[0])
    # initialize_create(iteration)
    feature = Feature(get_portfolioitem_id('feature')[0])
    initialize_create(feature)


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
    for _ in get_portfolioitem_id('feature'):
        feature = Feature(_)
        initialize(feature)


def main():
    initialize_mysql_table()
    # insert_mysql_test()

if __name__ == '__main__':
    main()
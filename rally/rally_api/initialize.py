from mysql_tools.mysql_curd import *
def initialize_mysql():
    tool = MysqlCurd('rally')
    tool.connect_mysql()
    f = open('../sql', 'r')
    sql = ''
    for _ in f.readlines():
        sql += _.strip()
    sql_list = sql.split('----------')
    for _ in sql_list:
        tool.curor.execute(_)
        tool.conn.commit()
    tool.close_connect()

if __name__ == '__main__':
    initialize_mysql()
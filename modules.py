import pymysql

from setting import *


class module():

    def __init__(self, table, database='movie'):
        self.db = pymysql.connect(sqlhost, sqluser, sqlpassword, database, sqlport, charset='utf8')
        self.cursor = self.db.cursor()
        self.table = '`{}`'.format(table)

    def _str(self, kwargs):
        keys = '(' + ','.join(map(str, kwargs.keys())) + ')'
        values = "('" + "','".join([i.replace("'", r"\'") for i in map(str, kwargs.values())]) + "')"
        values = values.replace("'NULL'", 'NULL')
        return keys, values

    def exe(self, sql):
        try:
            self.db.ping()
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except pymysql.Error as e:
            print(sql)
            print(e)

    def commit(self):
        return self.db.commit()

    def update(self, key, **kwargs):
        SET = ','.join([str(i) + "='" + str(kwargs[i]) + "'" for i in kwargs])
        return "UPDATE {0} SET {1} where {2};".format(self.table, SET, key)

    def select(self, key, *args):
        if '*' in args:
            args = [i[0] for i in self.exe('DESC {0};'.format(self.table))]
        print("SELECT {0} FROM {1} {2}".format(','.join(args), self.table, key))
        selectdata = self.exe("SELECT {0} FROM {1} {2}".format(','.join(args), self.table, key))
        result = []
        for i in selectdata:
            result.append({j: k for j, k in zip(args, i)})
        return result

    def insert(self, *args, **kwargs):
        if not kwargs:
            keys = ''
            values = args
        else:
            keys, values = self._str(kwargs)
        return 'INSERT INTO {0} {2} VALUES {1};'.format(self.table, values, keys)

#    def __del__(self):
#        self.db.close()

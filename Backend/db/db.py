import datetime
import random
import string
from pprint import pprint

import requests
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .config import URL_PARSE_LOGS, user, password, host, port, database

class Dbase:
    def __init__(self):
        self.connection = psycopg2.connect(user=user,
                                           # пароль, который указали при установке PostgreSQL
                                           password=password,
                                           host=host,
                                           port=port,
                                           database=database)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    def new_logs(self, branch, arch, name, hash, version, url, date, updated):
        self.cursor.execute("""INSERT INTO logs(branch, arch, name, hash, version, url, date, updated)
         VALUES(%s, %s, %s, %s, %s, %s, %s, %s""", (branch, arch, name, hash, version, url, date, updated))
        self.connection.commit()

    def gets_logs(self):
        self.cursor.execute("""SELECT * FROM logs""")
        return self.cursor.fetchall()

    def check_logs(self, date, updated):
        self.cursor.execute("""SELECT * FROM logs WHERE date = %s AND updated = %s""", (date, updated))
        return self.cursor.fetchone()

    def clear(self):
        self.cursor.execute("""DELETE FROM logs""")
        self.connection.commit()

    def get_log(self, id):
        self.cursor.execute("""SELECT * FROM logs WHERE id = %s""", (id,))
        return self.cursor.fetchone()

    def get_graphs(self):
        pass

    def get_graphs_period(self, startDate, endDate):
        pass

    def get_graphs_package(self, package):
        pass

    def get_graphs_package_period(self, package, startDate, endDate):
        pass

dbase = Dbase()

def get_db():
    return dbase


# парсинг логов из внешнего источника
def parse_logs(adres: str):
    res = requests.get(adres)
    try:
        if res.status_code == 200:
            for i in res.json()['ftbfs']:
                date1 = datetime.datetime.strptime(i['ftbfs_since'], '%Y-%m-%dT%H:%M:%S')
            date2 = datetime.datetime.strptime(i['updated'], '%Y-%m-%dT%H:%M:%S')
            print(date1)
            dbase.new_logs(i['branch'], i['arch'], i['name'], i['hash'], i['version'], i['url'], date1, date2)
    except Exception as e:
        print(f"Error with request: {str(e)}")



if __name__ == '__main__':
    parse_logs(URL_PARSE_LOGS)
    pprint(dbase.gets_logs())
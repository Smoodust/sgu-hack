import datetime
import random
import string
from pprint import pprint
from datetime import timedelta
import requests
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .config import URL_PARSE_LOGS, user, password, host, port, database
from .create_tables import create_tables

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
        create_tables()

    def new_logs(self, branch, arch, name, hash, version, url, updated, tbfs_since):
        self.cursor.execute("""INSERT INTO logs(branch, arch, name, hash, version, url, updated, tbfs_since)
         VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (branch, arch, name, hash, version, url, updated, tbfs_since))
        self.connection.commit()

    def get_logs(self):
        self.cursor.execute("""SELECT * FROM logs""")
        logs = self.cursor.fetchall()
        return [{
            'id': log[0],
            'branch': log[1],
            'arch': log[2],
            'name': log[3],
            'hash': log[4],
            'version': log[5],
            'url': log[6],
            'updated': log[7],
            'tbfs_since': log[8]
        } for log in logs]

    def check_logs(self, updated, tbfs_since):
        self.cursor.execute("""SELECT * FROM logs WHERE updated = %s AND tbfs_since = %s""", (updated, tbfs_since))
        return self.cursor.fetchone()

    def clear(self):
        self.cursor.execute("""DELETE FROM logs""")
        self.connection.commit()

    def get_log(self, id):
        self.cursor.execute("""SELECT * FROM logs WHERE id = %s""", (id,))
        log = self.cursor.fetchone()
        return {
            'id': log[0],
            'branch': log[1],
            'arch': log[2],
            'name': log[3],
            'hash': log[4],
            'version': log[5],
            'url': log[6],
            'updated': log[7],
            'tbfs_since': log[8]
        }
    

    def get_graphs(self):
        self.cursor.execute("""SELECT * FROM logs WHERE tbfs_since > NOW() - INTERVAL '1 month'""")
        logs = self.cursor.fetchall()
        count_logs = len(logs)
        time_counts = {}
        for log in logs:
            tbfs_date = log[8]  # tbfs_since
            updated_date = log[7]  # updated
            
            # Generate all dates between tbfs_since and updated
            current_date = tbfs_date
            while current_date <= updated_date:
                date_key = current_date.strftime("%Y-%m-%d")
                time_counts[date_key] = time_counts.get(date_key, 0) + 1
                current_date += timedelta(days=1)

        graphs = [{"time": time, "count": count} for time, count in time_counts.items()]
        graphs.sort(key=lambda x: x["time"])  # Sort by time
        return {
            'count_logs': count_logs,
            'graphs': graphs
        }

    def get_graphs_period(self, startDate, endDate):
        self.cursor.execute("""SELECT * FROM logs WHERE tbfs_since BETWEEN %s AND %s""", (startDate, endDate))
        logs = self.cursor.fetchall()
        count_logs = len(logs)
        time_counts = {}
        for log in logs:
            tbfs_date = log[8]  # tbfs_since
            updated_date = log[7]  # updated
            
            # Generate all dates between tbfs_since and updated
            current_date = tbfs_date
            while current_date <= updated_date:
                date_key = current_date.strftime("%Y-%m-%d")    
                time_counts[date_key] = time_counts.get(date_key, 0) + 1
                current_date += timedelta(days=1)

        graphs = [{"time": time, "count": count} for time, count in time_counts.items()]
        graphs.sort(key=lambda x: x["time"])  # Sort by time
        return {
            'count_logs': count_logs,
            'graphs': graphs
        }

    def get_graphs_package(self, package):
        self.cursor.execute("""SELECT * FROM logs WHERE name = %s""", ( package,))
        logs = self.cursor.fetchall()
        count_logs = len(logs)
        time_counts = {}
        for log in logs:
            tbfs_date = log[8]  # tbfs_since
            updated_date = log[7]  # updated
            
            # Generate all dates between tbfs_since and updated
            current_date = tbfs_date
            while current_date <= updated_date:
                date_key = current_date.strftime("%Y-%m-%d")
                time_counts[date_key] = time_counts.get(date_key, 0) + 1
                current_date += timedelta(days=1)

        graphs = [{"time": time, "count": count} for time, count in time_counts.items()]
        graphs.sort(key=lambda x: x["time"])  # Sort by time
        return {
            'count_logs': count_logs,
            'graphs': graphs
        }

    def get_graphs_package_period(self, package, startDate, endDate):
        self.cursor.execute("""SELECT * FROM logs WHERE name = %s AND tbfs_since BETWEEN %s AND %s""", (package, startDate, endDate))
        logs = self.cursor.fetchall()
        count_logs = len(logs)
        time_counts = {}
        for log in logs:
            tbfs_date = log[8]  # tbfs_since
            updated_date = log[7]  # updated
            
            # Generate all dates between tbfs_since and updated
            current_date = tbfs_date
            while current_date <= updated_date:
                date_key = current_date.strftime("%Y-%m-%d")        
                time_counts[date_key] = time_counts.get(date_key, 0) + 1
                current_date += timedelta(days=1)

        graphs = [{"time": time, "count": count} for time, count in time_counts.items()]
        graphs.sort(key=lambda x: x["time"])  # Sort by time
        return {
            'count_logs': count_logs,
            'graphs': graphs
        }
    
    def get_graphs_cluster(self, log_id):
        self.cursor.execute("""SELECT * FROM cluster WHERE log_id = %s""", (log_id,))
        clusters = self.cursor.fetchall()
        return clusters
    
    def new_cluster(self, log_id, Ox, Oy, Cluster_id):
        self.cursor.execute("""INSERT INTO cluster(log_id, Ox, Oy, Cluster_id) VALUES(%s, %s, %s, %s)""", (log_id, Ox, Oy, Cluster_id))
        self.connection.commit()

    def get_graphs_cluster_period(self, log_id, startDate, endDate):
        self.cursor.execute("""
            SELECT c.* 
            FROM cluster c
            JOIN logs l ON c.log_id = l.id
            WHERE c.log_id = %s AND l.tbfs_since BETWEEN %s AND %s
        """, (log_id, startDate, endDate))
        clusters = self.cursor.fetchall()
        return clusters
    
    def get_graphs_cluster_package(self, log_id, package):
        self.cursor.execute("""
            SELECT c.* 
            FROM cluster c
            JOIN logs l ON c.log_id = l.id
            WHERE c.log_id = %s AND l.name = %s
        """, (log_id, package))
        clusters = self.cursor.fetchall()
        return clusters
    
    def get_graphs_cluster_package_period(self, log_id, package, startDate, endDate):
        self.cursor.execute("""
            SELECT c.* 
            FROM cluster c
            JOIN logs l ON c.log_id = l.id
            WHERE c.log_id = %s AND l.name = %s AND l.tbfs_since BETWEEN %s AND %s
        """, (log_id, package, startDate, endDate))
        clusters = self.cursor.fetchall()
        return clusters
    
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
                dbase.new_logs(i['branch'], i['arch'], i['name'], i['hash'], i['version'], i['url'], date2, date1)
    except Exception as e:
        print(f"Error with request: {str(e)}")



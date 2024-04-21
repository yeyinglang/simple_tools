import sqlite3


# import schedule


class DataSource(object):
    def __init__(self, dbname):
        self.db = dbname

    # init_db
    def create_table(self, init_table_sql):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(init_table_sql)
            conn.commit()

    def insert(self, insert_sql, insert_values):
        res = None
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            res = cursor.execute(insert_sql, insert_values)
            conn.commit()
        return res
    def select(self, select_sql, select_values=None):
        res = None
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            if select_values:
                res = cursor.execute(select_sql, select_values)
            else:
                res = cursor.execute(select_sql)
        return res

    def delete(self, delete_sql, delete_values=None):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            if delete_values:
                cursor.execute(delete_sql, delete_values)
            else:
                cursor.execute(delete_sql)
            conn.commit()

    def update(self, update_sql, update_values):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(update_sql, update_values)
            conn.commit()


if __name__ == '__main__':
    init_summary_db = '''create table if not exists daily_plan( id INTEGER PRIMARY KEY AUTOINCREMENT,type varchar(50), plan TEXT NOT NULL, everyday_detail TEXT NOT NULL, everyday_summary TEXT NOT NULL)'''
    # init_memo_table_sql = 'create table if not exists memodb( id INTEGER PRIMARY KEY,priority varchar(50), content TEXT NOT NULL, remind_time TIMESTAMP NOT NULL)'

    data_source = DataSource('schedule.db')
    data_source.create_table(init_summary_db)
    insert_sql = "insert into summary_info(type, plan, everyday_detail, everyday_summary) values (?,?,?,?)"
    insert_values = ['typa', 'plan', 'everyday_detaila', 'everyday_summarya']
    data_source.insert(insert_sql, insert_values)
    select_vals = data_source.select('select * from summary_info')
    rows = select_vals.fetchall()
    for row in rows:
        print(row)
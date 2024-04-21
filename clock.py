from datetime import datetime
from datasource import DataSource
from daily import Daily
from week import Week

DATE_FORMAT = '%Y-%m-%d'


#  1、输入框
#  2、确认按钮
#  3、事件循环执行


def init_clock_table(datasource):
    daily = '''create table if not exists daily( id INTEGER PRIMARY KEY AUTOINCREMENT,
                        daily_date VARCHAR UNIQUE,
                        daily_plan VARCHAR , 
                        daily_detail VARCHAR , 
                        daily_summary VARCHAR ,
                        last_update VARCHAR)'''
    week_to_daily = '''create table if not exists week_to_daily( id INTEGER PRIMARY KEY AUTOINCREMENT,
                        daily_id INTEGER ,
                        week_id INTEGER )'''
    week = '''create table if not exists week( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        week_name VARCHAR UNIQUE,
                        week_summary VARCHAR ,
                        tobe_improved VARCHAR,
                        last_update VARCHAR
                        )'''
    month_to_week = '''create table if not exists month_to_week(id integer PRIMARY KEY AUTOINCREMENT,
                        month_id INTEGER,
                        week_id INTEGER )'''
    month = '''create table if not exists month(id INTEGER PRIMARY KEY AUTOINCREMENT,
                        month_name VARCHAR UNIQUE,
                        month_summary VARCHAR ,
                        tobe_improved VARCHAR,
                        last_update VARCHAR)'''
    datasource.create_table(daily)
    datasource.create_table(week)
    datasource.create_table(month)
    datasource.create_table(week_to_daily)
    datasource.create_table(month_to_week)

if __name__ == '__main__':
    '''
    1、每天的总结内容放在sqllite，每月、每周都总结，从sqllite获取；
    2、每天写清楚计划、每阶段任务、总结
    3、每天反思
    '''

    last_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    gap_mins = 30 * 60
    datasoure = DataSource('demo06db')
    init_clock_table(datasoure)
    daily = Daily(datasoure)

    while (True):
        # time.sleep(gap_mins)
        cur_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        # 晚10点，停止计时；等待第二天早上10点开始计时
        if datetime.now().hour > 22:
            # 第二天的开始
            daily.start_new_day()

        time_interval = str(last_time) + " -- " + str(cur_time) + " : "
        daily.remind_clock(time_interval)
        last_time = cur_time
        daily.select_all()

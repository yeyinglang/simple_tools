import tkinter as tk
from datetime import datetime
import time
from week import Week

from datasource import DataSource

DATE_FORMAT = '%Y-%m-%d'

class Daily():

    def __init__(self, datasource: DataSource):
        self.datasource =datasource

    def insert_daily(self):
        week = Week(self.datasource)
        week_cursor = week.insert()

        insert_daily_sql = 'insert into daily(daily_date,last_update) values (?, ?)'
        insert_daily_data = (datetime.now().strftime((DATE_FORMAT)), datetime.now())
        daily_cursor = self.datasource.insert(insert_daily_sql, insert_daily_data)

        week_to_daily_sql = 'insert into week_to_daily(week_id, daily_id) values(?,?)'
        self.datasource.insert(week_to_daily_sql, (week_cursor.lastrowid, daily_cursor.lastrowid))


    def query_daily(self):
        cols = ['id', 'daily_date', 'daily_plan', 'daily_detail', 'daily_summary']
        cur_date = datetime.now().strftime(DATE_FORMAT)
        select_sql = 'select ' + ','.join(cols) + ' from daily where daily_date = ?'
        daily = self.datasource.select(select_sql, (cur_date,))
        cur_info = daily.fetchone()
        if cur_info is None:
            self.insert_daily()
            cur_info =  self.datasource.select(select_sql, (cur_date,)).fetchone()
        return cur_info

    def update_daily(self, daily_plan, prev_detail, detail_this_time, summary_time_flag, daily_summary_val):
        update_sql = 'update daily set '
        update_data = []
        if daily_plan:
            update_sql += 'daily_plan=?, '
            update_data.append(daily_plan)
        cur_detail = None
        if prev_detail is None:
            cur_detail = detail_this_time
        elif detail_this_time is None:
            cur_detail = prev_detail
        else:
            cur_detail = prev_detail + detail_this_time
        if cur_detail:
            update_sql += 'daily_detail=?, '
            update_data.append(cur_detail)
        if summary_time_flag:
            update_sql += 'daily_summary=?'
            update_data.append(daily_summary_val)
        update_sql += 'last_update=? where daily_date=?'
        update_data.append(datetime.now().timestamp())
        update_data.append(datetime.now().strftime(DATE_FORMAT))
        self.datasource.update(update_sql, update_data)

    def remind_clock(self, time_interval):
        cur_info = self.query_daily()

        daily_plan = cur_info[2]
        prev_detail = cur_info[3]

        tk_root = tk.Tk()
        tk_root.minsize(width=800, height=800)
        tk_root.maxsize(width=800, height=1200)

        # 1、今日计划
        tk.Label(tk_root, text='Today Plan', width=100, height=1, font=('Georgia', 15)).pack(pady=10)
        plan_txt = tk.Text(tk_root, width=100, height=10)
        if daily_plan:
            plan_txt.insert('1.0', daily_plan)
        plan_txt.pack()

        # 2、每个时段进展
        tk.Label(tk_root, text='Every Interval Detail', width=100, height=1, font=('Georgia', 15)).pack(pady=10)
        text = tk.Text(tk_root, width=100, height=10)

        text.insert('1.0', time_interval)
        text.pack()

        # 3、每日8点至8.30之间总结
        summary_time_flag = False
        if datetime.now().hour == 20 and datetime.now().minute < 30:
            tk.Label(tk_root, text='Summary', width=100, height=1, font=('Georgia', 15)).pack(pady=10)
            summary_txt = tk.Text(tk_root, width=100, height=10)
            summary_txt.pack()
            summary_time_flag = True

        def get_input():
            # 1、plan
            daily_plan = plan_txt.get('1.0', 'end')
            # 2、Detail
            detail_this_time = text.get('1.0', 'end')
            # 3、summary
            daily_summary_val = None
            if summary_time_flag:
                daily_summary_val = summary_txt.get('1.0', 'end')

            # 4、write db
            self.update_daily( daily_plan, prev_detail, detail_this_time, summary_time_flag,
                              daily_summary_val)

            tk_root.destroy()

        tk.Button(tk_root, text="confirm", command=get_input, font=('Georgia', 15)).pack(pady=10)

        # 4、输出当前时刻之前的所有工作内容
        tk.Label(tk_root, text='Detail Processing', width=100, height=1, font=('Georgia', 15)).pack()
        label = tk.Label(tk_root, text=prev_detail, anchor='w', justify=tk.LEFT, wraplength=600)
        label.pack()

        # 将该弹出窗提示至最前面
        tk_root.lift()
        tk.mainloop()

    def start_new_day(self):
        hour_10 = 12 * 60 * 60
        time.sleep(hour_10)

    def select_all(self):
        sql = 'select * from daily '
        res = self.datasource.select(sql)
        for row in res.fetchall():
            print(row)

    def delete_all(self):
        sql = 'delete from daily'
        self.datasource.delete(sql)
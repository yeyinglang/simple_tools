from datasource import DataSource
import datetime
import tkinter as tk

class Week:
    '''
    下周写上周的总结，（可能不是周一）
    '''
    def __init__(self, datasource:DataSource):
        self.datasource = datasource

    def insert(self):
        '''
        插入一条周总结
        :param week_name: 第几周
        :return: None
        '''
        cur_week_info = self.get_cur_week_date()
        res_cursor = self.get_week_id(cur_week_info)
        if not res_cursor.fetchone():
            week_name = self.get_week_name()
            week_sql = 'insert into week(week_name, last_update) values(?,?)'
            res_cursor = self.datasource.insert(week_sql,(week_name, str(datetime.datetime.now())))
        return res_cursor

    def update(self,week_summary, tobe_improved):
        '''
        :param week: 每周总结
        :param tobe_improved: 每周待改进点
        :return:
        '''
        last_week_res = self.get_week_id(self.get_last_week_date())
        week_id= last_week_res.fetchone()[0]
        update_sql = 'update week set week_summary=' + week_summary + ' and tobe_improved='+ str(tobe_improved)+ ' where week_id=' + str(week_id)
        self.datasource.update(update_sql)


    def summary(self):
        tk_root = tk.Tk()
        tk_root.title('Week Summary')
        tk_root.minsize(width=800, height=600)
        tk_root.maxsize(width=800, height=1500)
        tk_root.resizable()
        last_weekly_summary = self.get_last_weekly_summary()
        last_info_txt = tk.Text(tk_root,  width=100 )
        last_info_txt.insert('1.0', ''.join(last_weekly_summary))
        last_info_txt.pack()


        tk.Label(tk_root, text='Last Week Summary',width=100, height=1, font=('Georgia', 15)).pack(pady=10)
        week_summary_txt = tk.Text(tk_root, width=100, height=10)
        week_summary_txt.pack()

        tk.Label(tk_root, text='Last Week To Be Improved', width=100, height=1, font=('Georgia', 15)).pack(pady=10)
        week_to_improved_txt = tk.Text(tk_root, width=100, height=10)
        week_to_improved_txt.pack()

        def update_result():
            summary_info = week_summary_txt.get('1.0','end')
            improved_info = week_to_improved_txt.get('1.0', 'end')
            self.update(summary_info, improved_info)
            tk_root.destroy()

        tk.Button(tk_root, text='Summary',command=update_result , font=('Georgia', 15)).pack()
        tk_root.lift()
        tk_root.mainloop()

    def get_week_id(self, last_week_info):
        place_holders = ','.join(['?'] * len(last_week_info))
        week_to_daily_sql = f"select week_id from week_to_daily where daily_id in (select id from daily where daily_date in ({place_holders}))"
        res = self.datasource.select(week_to_daily_sql, last_week_info)
        return res


    def get_cur_week_date(self):
        today = datetime.date.today()
        cur_weekdays = []
        for daydelta in range(today.weekday()+1):
            cur_weekdays.append(str(today-datetime.timedelta(days=daydelta)))
        return cur_weekdays

    def get_last_week_date(self):
        today = datetime.date.today()
        last_week_info = []
        daydelta = today.weekday()
        #  上周日---周一
        for i in range(1,8):
            last_week_info.append(str(today - datetime.timedelta(days=daydelta + i)))
        return last_week_info

    def get_week_name(self):
        today = datetime.date.today()
        weekday = today.weekday()
        monday = today-datetime.timedelta(days=weekday)
        sunday = today+ datetime.timedelta(days=(6-weekday))
        return str(monday) + '---' + str(sunday)

    def get_last_weekly_summary(self):
        # last_week_date = ','.join(self.get_last_week_date())
        last_week_date  = self.get_cur_week_date()
        place_holders = ', '.join(['?']*len(last_week_date))
        last_week_info_sql = f"select daily_date, daily_summary from daily where daily_date in ({place_holders})"
        last_week_summary_info = self.datasource.select(last_week_info_sql,last_week_date)
        last_weekly_summary = []
        for row in last_week_summary_info.fetchall():
            last_weekly_summary.append('\n'+row[0]+': '+ row[1]+'\n')
        return last_weekly_summary

    def select_all(self):
        sql = 'select * from week '
        res = self.datasource.select(sql)
        for row in res.fetchall():
            print(row)

if __name__ == '__main__':
    datasource = DataSource('demo06db')
    wee = Week(datasource)
    wee.summary()
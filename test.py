import datetime
import time

today = datetime.date.today()
weekday = today.weekday()
monday = today - datetime.timedelta(days=weekday)
print(today+ datetime.timedelta(days=(6-weekday)))
print(monday)

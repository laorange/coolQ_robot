import os
import time
import sched

os.environ['TZ'] = 'Asia/Shanghai'
# time.tzset() #Python time tzset() 根据环境变量TZ重新初始化时间相关设置。


t_Ymd = time.strftime("%Y%m%d", time.localtime())
t_HM = time.strftime("%H%M", time.localtime())
t_weekday = time.strftime("%A", time.localtime())

# print(t_HM)

s = sched.scheduler(time.time, time.sleep)


def verify_time(time2verify):
    pass

import os
import time
import sched
from send import send

os.environ['TZ'] = 'Asia/Shanghai'
# time.tzset() #Python time tzset() 根据环境变量TZ重新初始化时间相关设置。


t_Ymd = time.strftime("%Y%m%d", time.localtime())
t_HM = time.strftime("%H%M", time.localtime())
t_weekday = time.strftime("%A", time.localtime())

# print(t_HM)

s = sched.scheduler(time.time, time.sleep)


def verify_time(time2verify_ls):
    for time2verify in time2verify_ls:
        t_HM_now = time.strftime("%H%M", time.localtime())
        if t_HM_now == time2verify.time:
            send(time2verify.qq, time2verify.message)


def every_min_check():
    s.enter(60, 0, verify_time, )

import time
import sched
from send import send
from threading import Timer
from list_time2verify import Time2Verify
from list_time2verify import add_one_time_list
from list_time2verify import add_every_day_list
from list_time2verify import add_every_week_list
from list_time2verify import rewrite_one_time_list

t_Ymd = time.strftime("%Y%m%d", time.localtime())
t_HM = time.strftime("%H%M", time.localtime())
t_weekday = time.strftime("%A", time.localtime())

s = sched.scheduler(time.time, time.sleep)


def verify_time_send(time2verify_ls):
    for time2verify in time2verify_ls:
        t_H_M_now = time.strftime("%H:%M", time.localtime())
        t_YmdHM_now = time.strftime("%Y%m%d%H%M", time.localtime())
        print('qq:{},{},now:{}'.format(time2verify.qq, time2verify.send_time, t_YmdHM_now))  # #####################
        if t_YmdHM_now == time2verify.send_time:
            send(time2verify.qq, t_H_M_now + ' ' + time2verify.message)
            time2verify_ls.remove(time2verify)
    rewrite_one_time_list(time2verify_ls)
    return time2verify_ls


def verify_each_ls(time2verify_ls_ls):
    for time2verify_ls in time2verify_ls_ls:
        if isinstance(time2verify_ls, list) and len(time2verify_ls):
            verify_time_send(time2verify_ls)


def every_min_check():
    time2verify_ls_ls = [add_one_time_list(), add_every_day_list(), add_every_week_list()]
    s.enter(59, 0, every_min_check, ())
    verify_each_ls(time2verify_ls_ls)
    s.run()
    if time.strftime("%H%M", time.localtime()) == '0000':
        s.cancel()
        Timer(0, check_send_per_min, ())


def check_send_per_min():
    # time2verify_ls_ls = [add_one_time_list(), add_every_day_list(), add_every_week_list()]
    # time2verify_ls_ls[0] = [Time2Verify('', 2625835752, 'test1', '202007201006'),
    #                         Time2Verify('', 2625835752, 'test2', '202007201007')]
    every_min_check()


if __name__ == '__main__':
    check_send_per_min()

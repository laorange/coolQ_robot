import time
import sched
from send import send
from list_time2verify import Time2Verify
from list_time2verify import add_one_time_list
from list_time2verify import add_every_day_list
from list_time2verify import add_every_week_list

t_Ymd = time.strftime("%Y%m%d", time.localtime())
t_HM = time.strftime("%H%M", time.localtime())
t_weekday = time.strftime("%A", time.localtime())

# print(t_HM)

s = sched.scheduler(time.time, time.sleep)


def verify_time_send(time2verify_ls):
    for time2verify in time2verify_ls:
        t_HM_now = time.strftime("%Y%m%d%H%M", time.localtime())
        print(t_HM_now, time2verify.send_time)  # #####################
        if t_HM_now == time2verify.send_time:
            send(time2verify.qq, time2verify.message)
            time2verify_ls.remove(time2verify)
    return time2verify_ls


def verify_each_ls(time2verify_ls_ls):
    for time2verify_ls in time2verify_ls_ls:
        if isinstance(time2verify_ls, list) and len(time2verify_ls):
            verify_time_send(time2verify_ls)


def every_min_check(time2verify_ls_ls):
    s.enter(60, 0, every_min_check, (time2verify_ls_ls,))
    verify_each_ls(time2verify_ls_ls)
    s.run()


def check_send_per_min():
    time2verify_ls_ls = [add_one_time_list(), add_every_day_list(), add_every_week_list()]
    time2verify_ls_ls[0] = [Time2Verify('', 2625835752, 'test', '202007200918')]
    every_min_check(time2verify_ls_ls)


if __name__ == '__main__':
    check_send_per_min()

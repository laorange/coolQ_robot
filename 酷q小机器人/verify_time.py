import time
import sched
from send import send
from list_time2verify import Time2Verify


t_Ymd = time.strftime("%Y%m%d", time.localtime())
t_HM = time.strftime("%H%M", time.localtime())
t_weekday = time.strftime("%A", time.localtime())

# print(t_HM)

s = sched.scheduler(time.time, time.sleep)


def verify_time(time2verify_ls):
    for time2verify in time2verify_ls:
        t_HM_now = time.strftime("%Y%m%d%H%M", time.localtime())
        print(t_HM_now, time2verify.send_time)  # #####################
        if t_HM_now == time2verify.send_time:
            send(time2verify.qq, time2verify.message)


def every_min_check(time2verify_ls):
    s.enter(60, 0, every_min_check, (time2verify_ls,))
    verify_time(time2verify_ls)
    s.run()


if __name__ == '__main__':
    ls = []
    ls.append(Time2Verify('', 2625835752, 'test', '202007192231'))
    every_min_check(ls)

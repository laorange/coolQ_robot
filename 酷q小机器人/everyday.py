# everyday.py
import time
import sched

nth_circle = 0
# a_time = time.perf_counter()
s = sched.scheduler(time.time, time.sleep)


def perform():
    print("nth_circle:{}".format(nth_circle), end=', ')
    # print(time.perf_counter() - a_time)
    print(time.ctime())


def cal_delay(goal_time, period):
    global nth_circle
    result_delay = goal_time + nth_circle * period - time.time()
    while result_delay < 0:
        nth_circle += 1
        result_delay = goal_time + nth_circle * period - time.time()
    return result_delay


def mk_goal_time(goal_time_hm):
    if int(time.strftime('%H%M', time.gmtime())) > int(goal_time_hm):  # 今天的目标时间已经过了
        goal_time_str = time.strftime('%Y%m%d', time.gmtime(time.time() + 86400)) + goal_time_hm + '00'
    else:  # 今天的目标时间还没过
        goal_time_str = time.strftime('%Y%m%d', time.gmtime()) + goal_time_hm + '00'
    goal_time = time.mktime(time.strptime(goal_time_str, '%Y%m%d%H%M%S'))
    return goal_time


def circle(goal_time, func, period):
    global nth_circle
    delay = cal_delay(goal_time, period)
    # print('delay:{}'.format(delay), end=',')
    s.enter(delay, nth_circle, circle, (goal_time, func, period))
    func()
    nth_circle += 1


def every_day_inform(goal_time_hm, func, period=86400, nth_circle_init=0):
    global nth_circle
    nth_circle = nth_circle_init
    goal_time = mk_goal_time(goal_time_hm)
    s.enter(cal_delay(goal_time, period), 0, circle, (goal_time, func, period))
    s.run()


if __name__ == "__main__":
    every_day_inform("1051", perform, 2)

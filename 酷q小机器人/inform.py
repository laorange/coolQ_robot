# inform.py
import time
import sched
from threading import Timer
from send import send
from send import mk_goal_time
from send import cal_delay
from basic_functions import read_file2list


nth_circle = 0
# a_time = time.perf_counter()
s = sched.scheduler(time.time, time.sleep)
s1 = sched.scheduler(time.time, time.sleep)

t_Ymd = time.strftime("%Y%m%d", time.localtime())
t_weekday = time.strftime("%A", time.localtime())
# print(t_Ymd, t_weekday)


class PersonInform:
    def __init__(self, qq_sender, time_info, information):
        self.qq = qq_sender
        self.time = time_info
        self.info = information

    def send_timing(self):
        send(int(self.qq), self.info, self.time)


def check():
    file_name = 'user_data/everyday_infos/' + t_weekday + ".txt"
    person_inform_data_ls = read_file2list(file_name)
    print(person_inform_data_ls)
    # persons_ls = []

    def send_timing_issue(num):
        PersonInform(eval(person_inform_data_ls[num].split('^')[0]),
                     person_inform_data_ls[num].split('^')[1],
                     person_inform_data_ls[num].split('^')[2]).send_timing()

    for i in range(len(person_inform_data_ls)):
        person_inform_data_ls[i].split('^')
        Timer(1, send_timing_issue, args='i').run()
        print(1)
    #     persons_ls.append(PersonInform(person_inform_data_ls[i1].split('^')[0],
    #                                    person_inform_data_ls[i1].split('^')[1],
    #                                    person_inform_data_ls[i1].split('^')[2]))
    # print(persons_ls)

    # def class_send_timing(num):
    #     persons_ls[num].send_timing()
    #
    # for i2 in range(len(persons_ls)):
    #     print(persons_ls[i2].qq)
    #     #persons_ls[i2].send_timing()
    #     sched.scheduler(time.time, time.sleep).enter(0, 2-i2, class_send_timing(i2))
    #     sched.scheduler(time.time, time.sleep).run()


def every_day_check(goal_time_hm='0000', user_id=2625835752, message=''):
    goal_time = mk_goal_time(goal_time_hm)
    s.enter(cal_delay(goal_time), 0, every_day_check, (goal_time_hm, user_id, message))
    check()
    s.run()


# def start_every_day_check(goal_time_hm='0000', user_id=2625835752, message=''):
#     goal_time = mk_goal_time(goal_time_hm)
#     s.enter(cal_delay(goal_time), 0, every_day_check, (goal_time_hm, user_id, message))
#     s.run()


if __name__ == "__main__":
    check()


# def perform():
#     # print("nth_circle:{}".format(nth_circle), end=', ')
#     # # print(time.perf_counter() - a_time)
#     # print(time.ctime())
#     send(message='123456')
#
#
# def cal_delay(goal_time, period):
#     global nth_circle
#     result_delay = goal_time + nth_circle * period - time.time()
#     # print("1.delay:{}".format(result_delay))
#     while result_delay < 0:
#         nth_circle += 1
#         result_delay = goal_time + nth_circle * period - time.time()
#     return result_delay
#
#
# def mk_goal_time(goal_time_hm):
#     if int(time.strftime('%H%M', time.localtime())) > int(goal_time_hm):  # 今天的目标时间已经过了
#         goal_time_str = time.strftime('%Y%m%d', time.localtime(time.time() + 86400)) + goal_time_hm + '00'
#         tomorrow = 1
#         print("tomorrow:{}".format(tomorrow))
#     else:  # 今天的目标时间还没过
#         goal_time_str = time.strftime('%Y%m%d', time.localtime()) + goal_time_hm + '00'
#         tomorrow = 0
#         print("tomorrow:{}".format(tomorrow))
#     goal_time = time.mktime(time.strptime(goal_time_str, '%Y%m%d%H%M%S'))
#     return goal_time
#
#
# def circle(goal_time, func, period, user_id, message):
#     global nth_circle
#     delay = cal_delay(goal_time, period)
#     # print('delay:{}'.format(delay), end=',')
#     s.enter(delay, nth_circle, circle, (goal_time, func, period))
#     send(user_id, message)
#     nth_circle += 1
#
#
# def every_day_inform(goal_time_hm, func, user_id=2625835752, message='', period=86400, nth_circle_init=0):
#     global nth_circle
#     nth_circle = nth_circle_init
#     goal_time = mk_goal_time(goal_time_hm)
#     s.enter(cal_delay(goal_time, period), 0, circle, (goal_time, func, period, user_id, message))
#     s.run()
#
#
# def every_week_inform(goal_time_hm, func, user_id=2625835752, message='', period=604800, nth_circle_init=0):
#     global nth_circle
#     nth_circle = nth_circle_init
#     goal_time = mk_goal_time(goal_time_hm)
#     s.enter(cal_delay(goal_time, period), 0, circle, (goal_time, func, period, user_id, message))
#     s.run()
#
#
# def today_inform(goal_time_hm, user_id=2625835752, message=''):
#     goal_time = mk_goal_time(goal_time_hm)
#     s.enter(cal_delay(goal_time, 1), 0, send, (user_id, message))
#     s.run()
#     # cal_delay(goal_time, 1)
#
#
# if __name__ != "__main__":
#     # every_day_inform("1133", perform, 3)
#     today_inform("1145", message='123456789')
#     # send(message='123456')



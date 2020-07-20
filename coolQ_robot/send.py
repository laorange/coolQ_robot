# Send
# 用requests构造一个http post请求，post的数据填入相关信息：
# 参考知乎文章https://zhuanlan.zhihu.com/p/96892167?from_voters_page=true
import requests
import time
import sched

s = sched.scheduler(time.time, time.sleep)


def mk_goal_time(goal_time_hm, period=86400):
    # print(int(time.strftime('%H%M', time.localtime())))
    # print(int(goal_time_hm))
    if int(time.strftime('%H%M', time.localtime())) > int(goal_time_hm):  # 今天的目标时间已经过了
        print(int(time.strftime('%H%M', time.localtime())))
        print(int(goal_time_hm))
        goal_time_str = time.strftime('%Y%m%d', time.localtime(time.time() + period)) + goal_time_hm + '00'
        tomorrow = 1
        print("tomorrow:{}{}".format(goal_time_hm, tomorrow))
    else:  # 今天的目标时间还没过
        goal_time_str = time.strftime('%Y%m%d', time.localtime()) + goal_time_hm + '00'
        tomorrow = 0
        print("tomorrow:{}{}".format(goal_time_hm, tomorrow))
    goal_time = time.mktime(time.strptime(goal_time_str, '%Y%m%d%H%M%S'))
    return goal_time


def cal_delay(goal_time, period=86400, nth_circle_init=0):
    nth_circle = nth_circle_init
    # print(type(goal_time))
    result_delay = goal_time + nth_circle * period - time.time()
    while result_delay < 0:  # 前面mk_goal_time已经处理过了，此处nth_circle恒为0
        nth_circle += 1
        result_delay = goal_time + nth_circle * period - time.time()
    return result_delay


def send(user_id=2625835752, message='', timing=''):
    if len(timing) == 0:
        data = {
            'user_id': int(user_id),
            'message': message,
            'auto_escape': False
        }

        api_url = 'http://127.0.0.1:5700/send_private_msg'
        # 酷Q运行在本地，端口为5700，所以server地址是127.0.0.1:5700

        r = requests.post(api_url, data=data)
        print(r.text)
        return ''

    else:
        # mk_time_tomorrow_tuple = mk_goal_time(timing)
        delay = cal_delay(mk_goal_time(timing))
        s.enter(delay, 0, send, (user_id, message, ''))
        s.run()
        # return mk_time_tomorrow_tuple[1]  # tomorrow的值
        return ''


if __name__ == '__main__':
    print(send(message='你好', timing='1611'))

# class Send:
#     def __init__(self, user_id=2625835752, message=''):
#         """用于发送消息"""
#         self.user_id = user_id
#         self.message = message
#         self.data = {
#             'user_id': user_id,
#             'message': message,
#             'auto_escape': False
#         }
#
#     def send(self):
#         api_url = 'http://127.0.0.1:5700/send_private_msg'
#         # 酷Q运行在本地，端口为5700，所以server地址是127.0.0.1:5700
#         # api_url_group = 'http://127.0.0.1:5700/send_group_msg'
#
#         r = requests.post(api_url, data=self.data)
#         print(r.text)

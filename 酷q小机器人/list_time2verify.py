import time
import sched
from basic_functions import read_file2list

t_Ymd = time.strftime("%Y%m%d", time.localtime())
t_HM = time.strftime("%H%M", time.localtime())
t_weekday = time.strftime("%A", time.localtime())


class Time2Verify:
    def __init__(self, secret_code, qq, message, send_time):
        self.secret_code = secret_code
        self.qq = int(qq)
        self.message = message
        self.send_time = send_time


# every_week,调用星期N的任务
def add_every_week_list():
    time2verify_every_week_ls = []
    
    file_name = 'user_data/everyday_infos/' + t_weekday + ".txt"
    every_week_txt_ls = read_file2list(file_name)
    
    for num in range(len(every_week_txt_ls)):
        time2verify_every_week_ls.append(Time2Verify(every_week_txt_ls[num].split('^')[0],
                                                     eval(every_week_txt_ls[num].split('^')[1]),
                                                     every_week_txt_ls[num].split('^')[2],
                                                     t_Ymd+every_week_txt_ls[num].split('^')[3]))
    return time2verify_every_week_ls


def add_every_day_list():
    time2verify_every_day_ls = []
    every_day_txt_ls = read_file2list("user_data/everyday_infos/time2verify_every_day.txt")
    for num in range(len(every_day_txt_ls)):
        time2verify_every_day_ls.append(Time2Verify(every_day_txt_ls[num].split('^')[0],
                                                    eval(every_day_txt_ls[num].split('^')[1]),
                                                    every_day_txt_ls[num].split('^')[2],
                                                    t_Ymd+every_day_txt_ls[num].split('^')[3]))
    return time2verify_every_day_ls


def add_one_time_list():
    time2verify_one_time_ls = []
    one_time_txt_ls = read_file2list("user_data/everyday_infos/time2verify_one_time.txt")
    for num in range(len(one_time_txt_ls)):
        time2verify_one_time_ls.append(Time2Verify(one_time_txt_ls[num].split('^')[0],
                                                   eval(one_time_txt_ls[num].split('^')[1]),
                                                   one_time_txt_ls[num].split('^')[2],
                                                   one_time_txt_ls[num].split('^')[3]))
    return time2verify_one_time_ls


def rewrite_one_time_list(time2verify_one_time_ls):
    with open("user_data/everyday_infos/time2verify_one_time.txt", 'wt') as one_time_txt:
        for each_info in time2verify_one_time_ls:
            one_time_txt.write(each_info.secret_code+'^'+str(each_info.qq)+'^'
                               + each_info.message+'^'+each_info.send_time)


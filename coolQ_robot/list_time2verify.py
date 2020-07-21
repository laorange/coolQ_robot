import time
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

    file_name = 'user_data/everyday_infos/' + t_weekday + ".csv"
    every_week_csv_ls = read_file2list(file_name)

    # if isinstance(every_week_csv_ls[0], list):
    #     every_week_csv_ls = list(every_week_csv_ls)
    print('every_week_csv_ls', end='')
    print(every_week_csv_ls)
    for every_week_csv in every_week_csv_ls:
        time2verify_every_week_ls.append(Time2Verify(every_week_csv.split(',')[0],
                                                     int(every_week_csv.split(',')[1]),
                                                     every_week_csv.split(',')[2],
                                                     t_Ymd + every_week_csv.split(',')[3]))
    return time2verify_every_week_ls


def add_every_day_list():
    time2verify_every_day_ls = []
    every_day_csv_ls = read_file2list("user_data/everyday_infos/time2verify_every_day.csv")
    print('every_day_csv_ls', end='')
    print(every_day_csv_ls)
    if len(every_day_csv_ls):
        for num in range(len(every_day_csv_ls)):
            time2verify_every_day_ls.append(Time2Verify(every_day_csv_ls[num].split(',')[0],
                                                        int(every_day_csv_ls[num].split(',')[1]),
                                                        every_day_csv_ls[num].split(',')[2],
                                                        t_Ymd + every_day_csv_ls[num].split(',')[3]))
    return time2verify_every_day_ls


def add_one_time_list():
    time2verify_one_time_ls = []
    one_time_csv_ls = read_file2list("user_data/everyday_infos/time2verify_one_time.csv")
    print('one_time_csv_ls', end='')
    print(one_time_csv_ls)
    for num in range(len(one_time_csv_ls)):
        time2verify_one_time_ls.append(Time2Verify(one_time_csv_ls[num].split(',')[0],
                                                   int(one_time_csv_ls[num].split(',')[1]),
                                                   one_time_csv_ls[num].split(',')[2],
                                                   one_time_csv_ls[num].split(',')[3]))
    return time2verify_one_time_ls


def rewrite_one_time_list(time2verify_one_time_ls):
    with open("user_data/everyday_infos/time2verify_one_time.csv", 'wt') as one_time_csv:
        for each_info in time2verify_one_time_ls:
            one_time_csv.write(each_info.secret_code + ',' + str(each_info.qq) + ','
                               + each_info.message + ',' + each_info.send_time + '\n')


if __name__ == '__main__':
    pass

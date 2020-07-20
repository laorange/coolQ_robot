# input.py
from send import send
import time


def input_word(qq_sender, word, language='en'):
    send(qq_sender, 'sorry,由于实现该功能的思路不清晰，短期内不会继续开发\n已为您自动切换回聊天模式')
    code_change = 1
    return code_change


def input_inform_once(qq, message, send_time, code='m_day_one_time'):
    print('input_inform_once')
    with open('user_data/everyday_infos/time2verify_one_time.txt', 'at', encoding='ANSI') as time2verify_one_time_txt:
        time2verify_one_time_txt.write(code + '^' + str(int(qq)) + '^' + message + '^' + send_time + '\n')


def input_today_once_inform(qq, message, send_time, code='today_one_time'):
    print('input_today_once_inform')
    t_Ymd = time.strftime("%Y%m%d", time.localtime())
    with open('user_data/everyday_infos/time2verify_one_time.txt', 'at', encoding='ANSI') as time2verify_one_time_txt:
        time2verify_one_time_txt.write(code + '^' + str(int(qq)) + '^' + message + '^' + t_Ymd + send_time + '\n')


if __name__ == "__main__":
    pass


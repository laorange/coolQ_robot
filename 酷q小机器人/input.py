# input.py
from send import send
import time


def input_word(qq_sender, word, language='en'):
    send(qq_sender, 'sorry,由于实现该功能的思路不清晰，短期内不会继续开发\n已为您自动切换回聊天模式')
    code_change = 1
    return code_change


def input_inform_once(qq, message, send_time, secret_code=''):
    pass


def input_today_once_inform(qq, message, send_time, secret_code=''):
    t_Ymd = time.strftime("%Y%m%d", time.localtime())
    pass

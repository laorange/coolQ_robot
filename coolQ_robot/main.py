# main.py
import re
from flask import Flask, request
from json import loads
from threading import Thread
import time

from send import send
from review import review
from review import Review
from input import input_word
from input import input_inform_once
from input import input_today_once_inform
from robot import get_answer
from secret_code import secret_code
from secret_code import secret_code_off
from basic_functions import read_file2list
from user_list import generate_user_list
from user_list import add_2_user_list
from help_user import help_user


from verify_time import check_send_per_min

status = {}


def main(qq_sender, message_receive):
    m_once_inform = re.match(r'^(\d{12})(.*)', message_receive)
    m_today_once_inform = re.match(r'^(\d{4})(.*)', message_receive)
    m_every_day_inform = re.match(r'#EDAY(\d{4})(.*)', message_receive)
    m_every_week_inform = re.match(r'#EWK(\d)(\d{4})(.*)', message_receive)

    m_secret_code = re.match(r'#(.{8})(.*)', message_receive)
    m_secret_code_off = re.match(r'(\*)(.{8})(.*)', message_receive)
    m_emotion = re.match(r'(.*)(\[CQ:face,id=\d+\])(.*)', message_receive)
    m_image = re.match(r'\[CQ:image.*url=(.+)\]', message_receive)

    s_code_ls = read_file2list("user_data/secret_code/secret_code.txt")

    # 本次程序运行后，该用户第一次使用前的初始化
    if str(qq_sender) not in status.keys():  # 初次使用
        status[str(qq_sender)] = 0

    # 该用户第一次使用，记录该用户
    if str(qq_sender) not in generate_user_list():
        add_2_user_list(qq_sender)
        help_user(qq_sender)
        message_receive = ''

    # change the status code
    elif status[str(qq_sender)] in [9, 11, 12, 13, 14] and message_receive in ['m0', 'M0']:
        status[str(qq_sender)] = 0
        send(qq_sender, "已取消")
        message_receive = ''

    # 功能语句区
    # 切换回M0
    elif message_receive in ['m0', 'M0']:   # , '结束', 'end', 'over', 'stop'
        send(qq_sender, "已自动为您切换回聊天模式")
        status[str(qq_sender)] = 0

    # 一次性提醒
    elif m_once_inform:
        print('m_once_inform')
        t_YmdHM_now = time.strftime("%Y%m%d%H%M", time.localtime())
        if int(t_YmdHM_now) <= int(m_once_inform.group(1)):
            input_inform_once(qq_sender, m_once_inform.group(2), m_once_inform.group(1))
            send(qq_sender, '已添加提醒，将在{}.{}.{} {}:{}提醒您"{}"'.format(m_once_inform.group(1)[:4],
                                                                   m_once_inform.group(1)[4:6],
                                                                   m_once_inform.group(1)[6:8],
                                                                   m_once_inform.group(1)[8:10],
                                                                   m_once_inform.group(1)[10:],
                                                                   m_once_inform.group(2)))
        else:
            send(qq_sender, "该时间点已经过了哟，已忽略本次操作")
        message_receive = ''

    elif m_today_once_inform:
        print('m_today_once_inform')
        t_HM_now = time.strftime("%H%M", time.localtime())
        if int(t_HM_now) <= int(m_today_once_inform.group(1)):
            input_today_once_inform(qq_sender, m_today_once_inform.group(2), m_today_once_inform.group(1))
            send(qq_sender, '已添加提醒，将在今天{}提醒您"{}"'.format(m_today_once_inform.group(1)[:2] + ':' +
                                                         m_today_once_inform.group(1)[2:], m_today_once_inform.group(2)))
        else:
            send(qq_sender, "该时间点已经过了哟，已忽略本次操作")
        message_receive = ''

    # 循环提醒
    elif m_every_day_inform or m_every_week_inform:
        print('m_every_day_inform or m_every_week_inform')
        secret_code(message_receive[1:9], qq_sender, extra_info=message_receive[9:])
        message_receive = ''

    # help
    elif message_receive in ['help', 'Help', 'HELP', 'HELp', 'HElp']:
        help_user(qq_sender)
        message_receive = ''

        # 暗号功能
    elif m_secret_code:
        if m_secret_code.group(1) in s_code_ls:
            secret_code(m_secret_code.group(1), qq_sender, m_secret_code.group(2))
            send(qq_sender, '已激活该暗号对应功能...')
        else:
            send(qq_sender, '并没有这个暗号，请查证后稍后再试')
        message_receive = ''

    elif m_secret_code_off:
        send(qq_sender, 'sorry，该功能尚未完成，请过几天再试。已自动为您切换回聊天模式')
        message_receive = ''
        # elif message_check in s_code_ls:
        #     secret_code_off(message_receive)
        #     message_receive = ''
        #     send(qq_sender, '正在关闭该暗号对应功能...')

    # Mn切换模式
    elif message_receive in ['m1', 'M1']:   # , '输入', 'input', '+', '添加', '添加单词'
        status[str(qq_sender)] = 1
        send(qq_sender, '即将向当前数据库导入英语单词，\n'
                        '若想要取消请回复"m0"或"M0",\n'
                        '若确认要开始请直接回复想要导入的单词')

    elif message_receive in ['m2', 'M2']:   # , '复习', '我要复习', '学习', '我要学习'
        status[str(qq_sender)] = 2
        send(qq_sender, '即将开始复习当前数据库中的英语单词,\n'
                        '若想要取消请回复"m0"或"M0",\n'
                        '若确认开始请回复本次复习单词的个数(正整数)')

    elif message_receive in ['m3', 'M3']:   # , '输入', 'input', '+', '添加', '添加单词'
        status[str(qq_sender)] = 3
        send(qq_sender, '即将向当前数据库导入法语单词，\n'
                        '若想要取消请回复"m0"或"M0",\n'
                        '若确认要开始请直接回复想要导入的单词')

    elif message_receive in ['m4', 'M4']:   # , '复习', '我要复习', '学习', '我要学习'
        status[str(qq_sender)] = 4
        send(qq_sender, '即将开始复习当前数据库中的法语单词,\n'
                        '若想要取消请回复"m0"或"M0",\n'
                        '若确认开始请回复本次复习单词的个数(正整数)')

    elif message_receive in ['m9', 'M9']:
        send(qq_sender, '已进入反馈模式,此时您可以提交您在使用该机器人过程中遇到的问题。'
                        '同时，期待能够收到您的建议\n若您想要取消,请回复M0/m0')
        message_receive = ''
        status[str(qq_sender)] = 9

    # 根据状态执行功能
    elif status[str(qq_sender)] == 0:  # chat
        if message_receive in ['m0', 'M0']:
            send(qq_sender, "当前已经是聊天模式了,\n如果不是很清楚怎么切换模式,请输入help\n")
            message_receive = ''

        elif m_emotion:
            send(qq_sender, m_emotion.group(2))
            message_receive = m_emotion.group(1)+' '+m_emotion.group(3)

        elif m_image:
            send(qq_sender, '图片链接:'+m_image.group(1))
            message_receive = ''

        # 正常的chat:
        if message_receive.strip() != '':
            answer = get_answer(message_receive)
            send(qq_sender, answer)

    elif status[str(qq_sender)] == 11 or status[str(qq_sender)] == 13:
        try:
            num = eval(message_receive)
            if isinstance(num, int):
                if num > 0:
                    if status[str(qq_sender)] == 11:
                        rev = Review(qq_sender, 'en', num)
                    if status[str(qq_sender)] == 13:
                        rev = Review(qq_sender, 'fr', num)
                    status[str(qq_sender)] += 10  # 进入激活态2
                    rev.review()
            else:
                raise SyntaxError
        except:
            status[str(qq_sender)] = 0
            message_receive = ''
            send(qq_sender, "您的输入不正确\n已为您自动切换回聊天模式")

    elif status[str(qq_sender)] == 12:
        code_change = review(qq_sender, 'en')
        if code_change == 1:
            status[str(qq_sender)] = 0

    elif status[str(qq_sender)] == 13:
        code_change = input_word(qq_sender, message_receive, 'fr')
        if code_change == 1:
            status[str(qq_sender)] = 0

    elif status[str(qq_sender)] == 14:
        code_change = review(qq_sender, 'fr')
        if code_change == 1:
            status[str(qq_sender)] = 0

    elif status[str(qq_sender)] == 9:
        print('here')
        send(2625835752, '用户qq'+str(qq_sender)+'反馈：\n'+message_receive)
        send(qq_sender, '反馈成功!\n感谢您的反馈,我收到消息后会尽快与您联系\n已为自动您切换回聊天模式')
        message_receive = ''
        status[str(qq_sender)] = 0

    # end with changing the status code
    if status[str(qq_sender)] in [1, 2, 3, 4]:
        status[str(qq_sender)] += 10  # 11,12,13,14表明是的是对应模式的激活态1

    # 附加的激活项
    if status[str(qq_sender)] == 21:  # 复习英语单词的激活态②
        code_change = input_word(qq_sender, message_receive, 'en')
        if code_change == 1:
            status[str(qq_sender)] = 0

    elif status[str(qq_sender)] == 23:  # 复习法语单词的激活态②
        code_change = input_word(qq_sender, message_receive, 'fr')
        if code_change == 1:
            status[str(qq_sender)] = 0


def receive():
    bot_server = Flask(__name__)

    @bot_server.route('/api/message', methods=['POST'])
    # 路径是在酷Q配置文件里自定义的
    def server():
        data = request.get_data().decode('utf-8')
        data = loads(data)
        # print(data)
        qq_sender = data['sender']['user_id']
        nickname_sd = data['sender']['nickname']
        message_receive = data['message']
        print('{}(qq:{}):{}'.format(nickname_sd, qq_sender, message_receive))

        main(qq_sender, message_receive)

        return ''

    bot_server.run(port=5701)


if __name__ == "__main__":
    t1 = Thread(target=check_send_per_min)
    t2 = Thread(target=receive)
    t1.start()
    t2.start()


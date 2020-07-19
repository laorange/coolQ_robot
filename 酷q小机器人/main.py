# main.py
import re
from flask import Flask, request
from json import loads
import time  # 只用了.sleep()

from send import send
from review import review
from review import Review
from input import input_word
from robot import get_answer
from secret_code import secret_code
from secret_code import secret_code_off
from basic_functions import read_file2list
from user_list import generate_user_list
from user_list import add_2_user_list
from help_user import help_user

status = {}


def main(qq_sender, message_receive):
    # begin with changing the status code
    if str(qq_sender) not in status.keys():  # 初次使用
        status[str(qq_sender)] = 0

    if str(qq_sender) not in generate_user_list():
        add_2_user_list(qq_sender)
        help_user(qq_sender)
        message_receive = ''

    elif status[str(qq_sender)] in [11, 12, 13, 14, 19]:
        if message_receive in ['m0', 'M0']:
            status[str(qq_sender)] = 0
            send(qq_sender, "已取消")
            message_receive = ''

    # elif message_receive[0] in ['#', '*']:
    #     s_code_ls = read_file2list("/user_data/secret_code.txt")
    #
    #     if message_receive[0] == '*':
    #         message_check = '#' + message_receive[1:]
    #     if message_receive in s_code_ls:
    #         secret_code(message_receive)
    #         message_receive = ''
    #         send(qq_sender, '正在激活该暗号对应功能...')
    #     elif message_check in s_code_ls:
    #         secret_code_off(message_receive)
    #         message_receive = ''
    #         send(qq_sender, '正在关闭该暗号对应功能...')
    #     else:
    #         send(qq_sender, '并没有这个暗号，请查证后稍后再试')
    #         message_receive = ''

    elif message_receive in ['help', 'Help', 'HELP', 'HELp', 'HElp']:
        help_user(qq_sender)
        message_receive = ''

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

    elif message_receive in ['m0', 'M0']:   # , '结束', 'end', 'over', 'stop'
        status[str(qq_sender)] = 0

    elif message_receive in ['m9', 'M9']:
        send(qq_sender, '已进入反馈模式,此时您可以提交您在使用该机器人过程中遇到的问题。'
                        '同时，期待能够收到您的建议\n若您想要取消,请回复M0/m0')
        status[str(qq_sender)] = 9

    # 根据状态执行功能
    elif status[str(qq_sender)] == 0:  # chat
        if message_receive in ['m0', 'M0']:
            send(qq_sender, "当前已经是聊天模式了,\n如果想更改模式,\n"
                            "请输入m1/M1来导入单词,\n输入m2/M2来复习单词")
            message_receive = ''

        elif len(message_receive) > 8:
            if message_receive[:8] == '[CQ:face':
                send(qq_sender, message_receive)
                message_receive = ''
            elif message_receive[:9] == '[CQ:image':
                send(qq_sender, message_receive.split(',')[-1][4:-1])
                message_receive = ''
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
        send(2625835752, '[CQ:face,id=54]'+str(qq_sender)+'\n'+message_receive)
        send(qq_sender, '反馈成功!\n感谢您的反馈,我收到消息后会尽快与您联系\n已为自动您切换回聊天模式')
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
    receive()


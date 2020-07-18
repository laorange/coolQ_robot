# main.py
from flask import Flask, request
from json import loads
import time

from send import send
from review import review
from review import Review
from input import input_word
from robot import get_answer

status = {}


def main(qq_sender, message_receive):
    # begin with changing the status code
    if str(qq_sender) not in status.keys():  # 初次使用
        status[str(qq_sender)] = 0
        send(qq_sender, "您好,欢迎使用本机器人\n您可以参考下列指令来使用本机器人\n"
                        "M0(默认模式):\n"
                        "一、聊天模式，该模式下任何非功能性语句均调用小思(思知OwnThink)与您对话\n"
                        '二、在聊天模式下输入"暗号"可激活对应的循环推送功能\n'
                        '三、在聊天模式下可使用"备忘录功能":\n'
                        "  ①24小时内的一次性备忘\n   例:0809买票\n   (小时+分钟+事件,中间请不要间隔任何符号)"
                        '   机器人将会在当天08点09分提醒您"买票"\n   (若当天该时刻已过,将会在次日08点09分提醒)\n'
                        '  ②每日或每周的重复提醒属于循环推送，请使用"暗号"激活)')
        time.sleep(0.5)
        send(qq_sender, "M1:导入英语单词模式\n"
                        "M2:复习英语单词模式(尚未完成)\n"
                        # "L1:获取当前已导入的英语单词列表(尚未完成)\n"
                        "M3:导入法语单词模式\n"
                        "M4:复习法语单词模式(尚未完成)\n")
        time.sleep(0.5)
        send(qq_sender, "在M0(默认模式),可输入以下功能性语句:\n"                
                        'help:再次获取这些提示\n'
                        '输入M0/M1/M2/M3/M4(m可以小写)来切换模式'
                        '暗号(# + 8位密码)(功能正在开发):\n'
                        '#EVERYDAY:每日提醒(循环备忘录)\n'
                        '#EVERYW1K:每周提醒(循环备忘录)\n'
                        '#000001EN:每日推送部分已导入的英语单词以复习\n'
                        '#000001FR:每日推送部分已导入的法语单词以复习\n'
                        '......\n'
                        '解除暗号对应功能(* + 8位密码)(功能正在开发):\n')

    elif status[str(qq_sender)] in [11, 12, 13, 14]:
        if message_receive in ['m0', 'M0']:
            status[str(qq_sender)] = 0
            send(qq_sender, "已取消")
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
                        '若确认开始请回复任意其他语句')

    elif message_receive in ['m3', 'M3']:   # , '输入', 'input', '+', '添加', '添加单词'
        status[str(qq_sender)] = 3
        send(qq_sender, '即将向当前数据库导入法语单词，\n'
                        '若想要取消请回复"m0"或"M0",\n'
                        '若确认要开始请直接回复想要导入的单词')

    elif message_receive in ['m4', 'M4']:   # , '复习', '我要复习', '学习', '我要学习'
        status[str(qq_sender)] = 4
        send(qq_sender, '即将开始复习当前数据库中的法语单词,\n'
                        '若想要取消请回复"m0"或"M0",\n'
                        '若确认开始请回复任意其他语句')

    elif message_receive in ['m0', 'M0']:   # , '结束', 'end', 'over', 'stop'
        status[str(qq_sender)] = 0

    # 根据状态执行功能
    if status[str(qq_sender)] == 0:  # chat
        if message_receive in ['m0', 'M0']:  # , '结束', 'end', 'over', 'stop'
            send(qq_sender, "当前已经是聊天模式了,\n如果想更改模式,\n"
                            "请输入m1/M1来导入单词,\n输入m2/M2来复习单词")
            message_receive = ''
        if len(message_receive) > 8:
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
                    rev.review()
            else:
                raise SyntaxError
        except:
            pass

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

    # end with changing the status code
    if status[str(qq_sender)] in [1, 2, 3, 4]:
        status[str(qq_sender)] += 10  # 11,12,13,14表明是的是对应模式的激活态①

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


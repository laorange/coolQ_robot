from flask import Flask, request
from json import loads

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
                        "M0:聊天模式(默认模式),调用的是小思机器人(思知OwnThink)\n"
                        "备忘录功能:(聊天模式下):\n"
                        "格式:年月日时分 某事，例:202008082000 买票\n"
                        "(时间和事件之间,要间隔空格)"
                        '机器人将会在2020年08月08日20点00分提醒您"机票\n"'
                        "M1:导入英语单词模式\n"
                        "M2:复习英语单词模式(尚未完成)\n"
                        "L1:获取当前已导入的英语单词列表(尚未完成)\n"
                        "M3:导入法语单词模式\n"
                        "M4:复习法语单词模式(尚未完成)\n"
                        "L2:获取当前已导入的法语单词列表(尚未完成)\n"
                        "若需要切换模式请输入M0/M1/M2/M3/M4/L1/L2 (m,l均可以小写)\n"
                        'help:再次获取以上提示')

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

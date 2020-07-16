from flask import Flask, request
from json import loads

from send import send
from review import review
from input import input_word
from robot import get_answer

# 全局变量
status = {}


def main(qq_sender, message_receive):
    # begin with changing the status code
    if message_receive in ['m1', 'M1']:     # , '输入', 'input', '+', '添加', '添加单词'
        status[str(qq_sender)] = 1

    elif message_receive in ['m2', 'M2']:   # , '复习', '我要复习', '学习', '我要学习'
        status[str(qq_sender)] = 2

    elif message_receive in ['m0', 'M0']:   # , '结束', 'end', 'over', 'stop'
        status[str(qq_sender)] = 0

    # 功能函数
    def chat():
        answer = get_answer(message_receive)
        send(qq_sender, answer)

    # 根据状态执行功能
    if status[str(qq_sender)] == 0:
        chat()

    elif status[str(qq_sender)] == 3:
        input_word(message_receive)

    elif status[str(qq_sender)] == 4:
        review(qq_sender)

    # end with changing the status code
    if status[str(qq_sender)] in [1, 2]:
        status[str(qq_sender)] += 2


def receive():
    bot_server = Flask(__name__)

    @bot_server.route('/api/message', methods=['POST'])
    # 路径是在酷Q配置文件里自定义的
    def server():
        data = request.get_data().decode('utf-8')
        data = loads(data)
        # print(data)
        qq_sender = data['sender']['user_id']
        nickname_sd = data['sender']['str(qq_sender)']
        message_receive = data['message']
        print('{}(qq:{}):{}'.format(nickname_sd, qq_sender, message_receive))

        main(qq_sender, message_receive)

        return ''

    bot_server.run(port=5701)


if __name__ == "__main__":
    receive()

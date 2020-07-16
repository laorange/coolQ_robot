from flask import Flask, request
from json import loads

from send import send
from review import review
from input import input_word
from robot import get_answer


def main(nickname_sender, qq_sender, message_receive):
    if message_receive in ['复习', '我要复习', '学习', '我要学习']:
        review()
    elif message_receive in ['输入', 'input', '+', '添加', '添加单词']:
        input_word()
    else:
        answer = get_answer(message_receive)
        send(qq_sender, answer)

    pass


def receive():
    bot_server = Flask(__name__)

    @bot_server.route('/api/message', methods=['POST'])
    # 路径是你在酷Q配置文件里自定义的
    def server():
        data = request.get_data().decode('utf-8')
        data = loads(data)
        # print(data)
        qq_sender = data['sender']['user_id']
        nickname_sender = data['sender']['nickname']
        message_receive = data['message']
        print('{}(qq:{}):{}'.format(nickname_sender, qq_sender, message_receive))

        main(nickname_sender, qq_sender, message_receive)

        return ''

    bot_server.run(port=5701)


if __name__ == "__main__":
    receive()

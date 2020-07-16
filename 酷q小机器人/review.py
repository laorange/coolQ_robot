# review.py
from send import send


def review(qq_sender, language='en'):
    send(qq_sender, 'sorry,该模式功能尚未完成,请几天后再试\n已为您自动切换回聊天模式')
    pass

    code_change = 1
    return code_change

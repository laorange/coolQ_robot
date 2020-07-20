# review.py
from send import send


def review(qq_sender, language='en'):
    send(qq_sender, 'sorry,由于实现该功能的思路不清晰，短期内不会继续开发\n已为您自动切换回聊天模式')
    code_change = 1
    return code_change


class Review:
    def __init__(self, qq_sender, language, num):
        self.qq_sender = qq_sender
        self.language = language
        self.num = num

    def review(self):
        pass

# Send
# 用requests构造一个http post请求，post的数据填入相关信息：
# 参考知乎文章https://zhuanlan.zhihu.com/p/96892167?from_voters_page=true
import requests


def send(user_id=2625835752, message=''):
    data = {
        'user_id': user_id,
        'message': message,
        'auto_escape': False
    }

    api_url = 'http://127.0.0.1:5700/send_private_msg'
    # 酷Q运行在本地，端口为5700，所以server地址是127.0.0.1:5700

    r = requests.post(api_url, data=data)
    print(r.text)
    return ''


if __name__ == '__main__':
    send(message='你好')

# class Send:
#     def __init__(self, user_id=2625835752, message=''):
#         """用于发送消息"""
#         self.user_id = user_id
#         self.message = message
#         self.data = {
#             'user_id': user_id,
#             'message': message,
#             'auto_escape': False
#         }
#
#     def send(self):
#         api_url = 'http://127.0.0.1:5700/send_private_msg'
#         # 酷Q运行在本地，端口为5700，所以server地址是127.0.0.1:5700
#         # api_url_group = 'http://127.0.0.1:5700/send_group_msg'
#
#         r = requests.post(api_url, data=self.data)
#         print(r.text)

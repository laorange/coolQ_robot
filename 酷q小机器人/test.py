import re

message_receive = "[CQ:image,file=99AD14A7FFD13BAEA8C6AAAF19037156.jpg,url=(https://c2cpicdw.qpic.cn/offpic_new/1938466844//1938466844-3991116225-99AD14A7FFD13BAEA8C6AAAF19037156/0?term=2)]"
m_image = re.match(r'\[CQ:image.*url=\((http.+)\)\]', message_receive)
print(m_image.group(1))

m_today_once_inform = re.match(r'(\d{4})(.*)', message_receive)
m_once_inform = re.match(r'(\d{12})(.*)', message_receive)
m_secret_code = re.match(r'#(.{8})(.*)', message_receive)
m_secret_code_off = re.match(r'(\*)(.{8})(.*)', message_receive)
m_emotion = re.match(r'(.*)([CQ:face,id=\d+])(.*)', message_receive)
m_image = re.match(r'\[CQ:image.*url=\((http.+)\)\]', message_receive)

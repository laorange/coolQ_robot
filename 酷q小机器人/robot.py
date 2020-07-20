import requests


# 以下是机器人小思部分！！！！↓
def get_answer(text):    # 获取思知机器人的回复信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'https://robot.ownthink.com/',
    }

    def get_data(text_for_data):  # 请求思知机器人API所需要的一些信息
        pre_data = {
            "appid": "5d04bed96ac912c3c9f172e201504659",
            "userid": "Ak9c76Wl",
            "spoken": text_for_data,
        }
        return pre_data

    data = get_data(text)
    url = 'https://api.ownthink.com/bot'  # API接口
    response = requests.post(url=url, data=data, headers=headers)
    response.encoding = 'utf-8'
    result = response.json()
    answer = result['data']['info']['text']
    return answer


if __name__ == "__main__":
    get_answer("你好")

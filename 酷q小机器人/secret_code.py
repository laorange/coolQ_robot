# secret_code.py
def secret_code(code, qq, extra_info=''):
    if code[:4] == 'EDAY':
        with open(r'user_data\everyday_infos\time2verify_every_day.txt', 'at') as time2verify_every_day_txt:
            time2verify_every_day_txt.write(code+'^'+str(int(qq))+'^'+extra_info+'^'+code[4:]+'\n')

    if code[:3] == 'EWK':
        if code[3] == '1':
            week_day = 'Monday'
        elif code[3] == '2':
            week_day = 'Tuesday'
        elif code[3] == '3':
            week_day = 'Wednesday'
        elif code[3] == '4':
            week_day = 'Thursday'
        elif code[3] == '5':
            week_day = 'Friday'
        elif code[3] == '6':
            week_day = 'Saturday'
        elif code[3] == '7':
            week_day = 'Sunday'
        with open("user_data\\everyday_infos\\"+week_day+".txt", 'at') as time2verify_every_day_txt:
            time2verify_every_day_txt.write(code+'^'+str(int(qq))+'^'+extra_info+'^'+code[4:]+'\n')

    pass


def secret_code_off(code, qq):
    pass

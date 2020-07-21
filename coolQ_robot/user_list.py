#user_list.py
from basic_functions import read_file2list


def generate_user_list():
    user_ls = read_file2list('user_data/private_space/user_list.csv')
    return user_ls


def add_2_user_list(new_user_qq):
    with open('user_data/private_space/user_list.csv', 'at') as user_ls_csv:
        user_ls_csv.write(str(new_user_qq)+'\n')
        user_ls_csv.close()


if __name__ == "__main__":
    pass

from threading import Thread

from receive import receive
from verify_time import check_send_per_min

if __name__ == '__main__':
    t1 = Thread(target=check_send_per_min)
    t2 = Thread(target=receive)
    t1.start()
    t2.start()

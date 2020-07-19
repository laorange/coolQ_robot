from send import send
import time
from threading import Timer

Timer(5, send, args=(2625835752, '2')).run()
Timer(2, send, args=(2625835752, '1')).run()
for i in range(5):
    print(i+1)
    time.sleep(0.99)

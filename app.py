from app import app
from threading  import Thread
import time

# def task(args):
#     print('done task ' + str(args))

# num = 1

# def func():
#     global num
#     while(num > 0):
#         for i in range(num):
#             time.sleep(5)
#             Thread(target=task, args=list([i])).start()
#         num = int(input('Enter a number: '))

# Thread(target=func).start()

if __name__ == '__main__':
    app.run(port=1080, debug=True)

    
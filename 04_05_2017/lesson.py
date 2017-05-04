# import module1 as m
import sys
import pprint

################## Threading
import threading

# l = threading.Lock()  # Бинарный симафор
# a = 0
#
# def f():
#     global a
#     for i in range(10000):
#         l.acquire()      # захватить. Никак не обращается к планировщику.
#         a += 1
#         l.release()      # отпустить
#
# ts = []

import urllib.request
import time

# r = urllib.request.urlopen('http://mail.ru')

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))

if __name__ == '__main__':

    import queue
    q = queue.Queue()


    def get(i):
        while True:
            url = q.get()
            if url is None:
                break
            r = urllib.request.urlopen('http://mail.ru')
            print(i, len(r.read()))
            q.task_done()

    # with Profiler as p:
    for i in range(5):
        t = threading.Thread(target=get, args=(i, ))
        t.start()

    for i in range(20):
        q.put('http://mail.ru')

    q.join() # Дождаться чтобы все выполнили свои задачи

    for i in range(5):
        q.put(None)

    # for i in range(2):
    #     t = threading.Thread(target=f)
    #     t.start()  # Поставить поток в очередь что бы он начал выполняться
    #     ts.append(t)
    #
    # for t in ts:
    #     t.join()  # Ждет завершения потоков.

    # print(a)

    # pprint.pprint(sys.modules)
    # print(m.A)
    # m.A = 20
    # print(m.A)
    #
    # a = 20
    # m.a = 2
    # print(m.f(5))
    # pprint.pprint(sys.path)
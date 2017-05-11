# process

if __name__ == '__main__':
    import multiprocessing
    import time

    # a = 0

    # def f():
    #     global a
    #     for a in range(10000):
    #         a += 1
    #     print(a)

    # # a = multiprocessing.Value('i', 0)
    #
    # def f():
    #     global a
    #     for a in range(10000):
    #         a += 1
    #     q.put(a)
    #
    # q = multiprocessing.Queue()
    #
    # for _ in range(2):
    #     p = multiprocessing.Process(target=f)
    #     p.start()
    #
    # for _ in range(2):
    #     # print("atata: {}".format(q.get()))
    #     a += q.get()

    # ps = []
    # for i in range(5):
    #     p = multiprocessing.Process(target=f)
    #     p.start()
    #     ps.append(p)
    #
    # for p in ps:
    #     p.join()  # Барьерная синхронизация гаранируют, что все процессы завершатся

    a = multiprocessing.Value('i', 0)


    def f():
        for i in range(10000):
            a.value += 1

    q = multiprocessing.Queue()

    ps = []
    for _ in range(2):
        p = multiprocessing.Process(target=f)
        p.start()
        ps.append(p)

    for p in ps:
        p.join()

    print(a.value)

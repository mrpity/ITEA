
# Sockets server

if __name__ =='__main__':
    import socket
    import threading
    import select

    # Однопользовательский сокет
    # s = socket.socket()
    # s.bind(('localhost', 5000))
    # s.listen(5)
    # print('Waiting...')
    # c, a = s.accept()
    # print('Connected:', a)
    # print(c, c is s)
    #
    # data = c.recv(1024)
    # print(data)
    #
    # c.sendall(data)
    # c.close()
    # s.close()


    # Многопользовательский сокет

    # def handle(c):
    #     while True:
    #         data = c.recv(1024)
    #         if not data:         # признак закрытия соедения с клиентом, если данных нет.
    #             c.close()
    #             break
    #         print(data)
    #         c.sendall(data)
    #
    # s = socket.socket()
    # s.bind(('localhost', 5000))
    # s.listen(5)
    # print('Waiting....')
    # while True:
    #     c, a = s.accept()
    #     print('Connected:', a)
    #
    #     t = threading.Thread(target=handle, args=(c, ))
    #     t.start()

    # Асинхронный подход. Не создает новых потоков для клиентов. Все клиенты в одном потоке

    def handle(c):
        data = c.recv(1024)
        if not data:         # признак закрытия соедения с клиентом, если данных нет.
            connections.remove(c)
            c.close()
            return
        print(data)
        c.sendall(data)

    s = socket.socket()
    s.bind(('localhost', 5000))
    s.setblocking(False)  # Сокеты не будут останавливаться и ожидать что в сокете что-то появится
    s.listen(5)
    print('Waiting...')
    connections = [s]     # Сокеты ожидающие чтение
    while True:
        r_s, _, _ = select.select(connections, [], [])
        for r in r_s:
            if r == s:
                c, a = s.accept()
                print('Connected:', a)
                connections.append(c)
            else:
                handle(r)

# socket client

if __name__ == '__main__':

    import socket
    import time

    # Один пользователь
    # s = socket.socket()
    # s.connect(('localhost', 5000))
    # s.sendall(b'Hello')
    # data = s.recv(1024)
    # print(data)
    # s.close()


    # Много пользователей
    # s = socket.socket()
    # s.connect(('localhost', 5000))
    # while True:
    #     s.sendall(b'Hello')
    #     data = s.recv(1024)
    #     print(data)
    #     time.sleep(2)
    # # s.close()
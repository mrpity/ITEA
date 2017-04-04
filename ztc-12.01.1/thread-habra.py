import threading
import time

def writer(x, event_for_wait, event_for_set):
    for i in xrange(4):
        event_for_wait.wait() # wait for event
        event_for_wait.clear() # clean event for future
        print x
        event_for_set.set() # set event for neighbor thread

# init events
e1 = threading.Event()
e2 = threading.Event()

# init threads
t1 = threading.Thread(target=writer, args=(0, e1, e2))
t1.setName('zopa')
t2 = threading.Thread(target=writer, args=(1, e2, e1))

# start threads
t1.start()
t2.start()

print t1.isAlive()
print t2.isAlive()

e2.set() # initiate the first event


print t1.getName()
print t2.getName()
# join threads to the main thread
t1.join()
t2.join()


def proc(n, s):
    time.sleep(s)
    print 'Thread', str(n), 'finished'


for x in range(1, 4):
    print 'Thread', str(x), 'started'
    print 'Count of active threads ', threading.activeCount()

    if (x == 1):
        threading.Thread(target=proc, args=[x, 3]).start()
    elif (x == 2):
        threading.Thread(target=proc, args=[x, 1]).start()
    elif (x == 3):
        threading.Thread(target=proc, args=[x, 2]).start()
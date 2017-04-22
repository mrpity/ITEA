"""
a = 0

def f():
    global a
    a +=1
    return a

for i in iter(f, 5):  ## Does not show last <<i>>
    print(i)



class MyList:
    def __init__(self, l=[]):
        self._l = list(l)     # save list state l.copy()  ## self._l = list(l)

    def __repr__(self):
        return repr(self._l)

    def add(self, a):
        self._l.append(a)

    def __len__(self):         # magic method for <<len>> func
        return len(self._l)

    def __bool__(self):       # exec throw <<bool>>
        return bool(self._l)

    def __contains__(self, obj):  # Is obj is contaiter or not?  # throw <<in>> operator
        return obj in self._l

    def __setitem__(self, index, value):  # set value by index
        self._l[index] = value

    def __getitem__(self, index):   # get value by index
#        return self._l[index]
#        print(index)
         if isinstance(index, int):
             return self._l[index]
         elif isinstance(index, tuple):
             return [self._l[i] for i in index ]
         elif index == ...:
             return self._l.copy()
         else:
             raise IndexError

    def __iter__(self):
        for i in self._l:
            yield i
#        return iter(self._l)
#        return MyListIterator(self._l)

class MyListIterator:
    def __init__(self, l):
        print('Iter')
        self._l = l
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        print('Next')
        self._i += 1
        if self._i == len(self._l) +1:
            raise StopIteration
        return self._l[self._i - 1]

if __name__ == '__main__':
#    l = MyList([1,2,3])
#    print(l)
#    l1 = [1,2,3]
#    l = MyList(l1)
#    print(l)
#    l1[0] = 0
#    print(l)
#    print(len(l))
#    print(bool(l))
#    print(1 in l)
#    l[0] = 4
#    print(l)
#    l = MyList(range(10))
#    print(l)
#    print(l[...])
#    print(l[1,2,3,4])
#
#    for i in l:
#        print(i)
    l = MyList([1,3,4])
    for i in l:
        for j in l:
            print(i,j)
            
################################3

def infinity_list():
    i = 0
    while True:
        yield i
        i += 1

if __name__ == '__main__':
    g = infinity_list()
    print(next(g))

    for i in infinity_list():
        if i*i > 100:
            break
        print(i, i*i)

    import itertools     ## iterators
    print(list(itertools.takewhile(lambda x: x < 100, (x * x for x in itertools.count(0)))))

    l = [0] * 5 + [1] * 2 + [0] * 3 + [1] * 5
    print(l)
    for i,j in itertools.groupby(l):
        print(i, list(j))
        print(i, len(list(j)))
        
"""

#################### Coroutine

def coroutine(f):
    gen = f()
    next(gen)
    return gen

@coroutine
def f():
    i = yield
    print('f:', i)
    i = yield i + 1
    print('f:', i)
    i = yield i + 1
    print('f:', i)
#    yield i + 1

def main():
    i = f.send(0)
    print('main:', i)
    i = f.send(i + 1)
    print('main:', i)
    i = f.send(i + 1)
    print('main:', i)

main()

















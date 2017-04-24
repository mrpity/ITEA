"""
class CSV:
    def load(self):
        print('CSV load')
        return {'Bill': 911}

    def save(self, d):
        print('CSV save')

class JSON:
    def load(self):
        print('JSON load')
        return {'Bill': 911}

    def save(self, d):
        print('JSON save')



CONFIG = {
    'dumper': 'CSV',
}

if CONFIG['dumper'] == 'CSV':
    dumper = CSV()
elif CONFIG['dumper'] == 'JSON':
    dumper = JSON()

phonebook = dumper.load()

# Model

dumper.save(phonebook)
"""

# print('yield')
def f():
    for i in range(5):
        yield i
        print(i)

# g = f()

# print(next(g))
############################################################################
print("-------------------------------------")

def f():
    fn = open('test.txt', 'rt')
    for line in fn:
        try:
            yield line
        except GeneratorExit:
            fn.close()
            break

# g = f()

# print(next(g))
# print(next(g))
# print(next(g))
#
# g.close()
# print(next(g))

# print(dir(g))

# g.throw(ValueError)  ## Можно бросать исключение в генератор. Управлять генератором извне

#################################

class A:
    def __init__(self, f):
        self.f = f
        self.a = 1


a = A(lambda x: 2 * x)

print(vars(a))
print(a)

import pickle
# pickle.dumps(a)

class B:
    def __init__(self, f):
        self.f = f
        self.a = 1

    def __getstate__(self):
        print('Get state')
        d = self.__dict__.copy()
        del d['f']
        return d

    def __setstate__(self, obj):
        print("Set state")
        self.__dict__ = obj
        self.f = lambda x: 2 * x

# a = B(lambda x: 2 * x)
# s = pickle.dumps(a)
# b = pickle.loads(s)
# print(vars(b))

class C:
    def __init__(self):
        self.a = 1

    def __enter__(self):
        print('Enter')

    def __exit__(self, *args, **kwargs):
        print('Exit')

with C() as c:            ### It's the same as  --- c = C()
    pass

print('-------------------------------------------')


class Multipler:

    def __init__(self, n):
        self._n = n

    def __call__(self, x):
        print('Call')
        return self._n * x

double = Multipler(2)

print(double(2))


class scale:

    def __init__(self, n):
        self._n = n

    def __call__(self, f):
        def wrapper(x):
            return f(x * self._n)
        return wrapper

@scale(5)
def get_area(x):
    return x * x

print(get_area(5))

##### РЕКУРСИВНАЯ функция

def fib(n):
    if n < 2:
        return n
    return fib(n -1) + fib(n - 2)

print(fib(20))


class memo:

    def __init__(self):
        self._state = {}

    def __call__(self, f):
        def wrapper(n):
            if n not in self._state:
                self._state[n] = f(n)
            return self._state[n]
        return wrapper


@memo()
def fib(n):
    if n < 2:
        return n
    return fib(n -1) + fib(n -2)


import profile
# print(fib(10))
# profile.run('fib(20)')

m = memo()

@m
def fib(n):
    if n < 2:
        return n
    return fib(n -1) + fib(n -2)

# profile.run('fib(10)')

print(fib(10))
print(m._state)


print('--------------------------')

class F:
    def __new__(cls):
        return 42

g = F()

print(g)
print(type(g))

print('-----------------------------------------------------')

class Car:

    def run(self):
        print('I am car')

class Truck:

    def run(self):
        print('I am truck')

class Vehicle:

    def __new__(cls, type_):
        if type_ == 'Car':
            return Car()
        elif type_ == 'Truck':
            return Truck()
        else:
            raise ValueError

vehicles = ['Car', 'Car', 'Truck', 'Car']

vehicles = [Vehicle(x) for x in vehicles]

import pprint
pprint.pprint(vehicles)

for vehicles in vehicles:
    vehicles.run()

print('-------------------------------------------------------------')

def f():
    class A:
        def f(self):
            print('I am class A')
    return A

c = f()
print(c)
a = c()
a.f()


print('-------------------------------------------------------------')

class Singleton():

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance


s = Singleton()
s1 = Singleton()

print(s is s1)        ## Любой Синглтон будет одним и тем же экземпляром класса.

class A:
    db_conn = ...

## Удаление атрибута
del Singleton._instance


####### PAttern Observer

def a():
    print('a')

def b():
    print('b')

def c():
    print('c')

class Notifier:

    def __init__(self):
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            res = f(*args, **kwargs)
            for observer in self.observers:
                observer()
            return res
        return wrapper

# def notify(f):
#     def wrapper(*args, **kwargs):
#         res = f(*args, **kwargs)
#         for observer in sobservers:
#             observer()
#         return res
#     return wrapper

# @notify
notifier = Notifier()

@notifier
def f():
    return 42

print(f())

notifier.register(a)
print(f())

# observers.append(b)
# print(f())
# observers.append(a)
# print(f())

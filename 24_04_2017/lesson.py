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
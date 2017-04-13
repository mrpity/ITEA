
"""
class ReprMixin:
    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ', '.join([
                "{}={}".format(name, value)
                for name, value in self.__dict__.items()
                ]
            )
        )

class EquelMixin:
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__dict__ == other.__dict__

class Person(ReprMixin, EquelMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

if __name__ == "__main__":
    p = Person('Bill', 23)
    print(p)
    print(Person('Bill', 23) == Person('Bill', 23))
#######################################################################################

import numbers

class Number:
    def __init__(self, n):
        self._n = n
    def __repr__(self):
        return "Number ({})".format(self._n)
    def __add__(self, other):
        if isinstance(other, numbers.Number):  ##  (int, float, complex) ~~ numbers.Number
            return Number(self._n + other)
        return Number(self._n + other._n)
    def __radd__(self, other):
        return self.__add__(other)  ## __radd__ - вызывается с параметрами в обратном порядке
    def __iadd__(self, other):       ## это эквивалентно +=
        return self.__add__(other)


if __name__ == "__main__":
    n = Number(5)
    print(n)
    print(Number(5) + Number(4))
    print(Number(5) + 3)
    print(5 + Number(5))


import collections   ## определены спец. интерфейсы UserList UserDict UserString. Содержат data -- точно такое же как и self

class MyList(collections.UserList):
    def sum(self):
        s = 0
        for i in self.data:   ## Для читабельности. Если не наследоваться от collections.UserList просто for по self делать
            s += i
        return s

if __name__ == "__main__":

    l = MyList([2,4,5,6])
    print(l)
    print(dir(l))
    print(l.sum())

"""

################################# UNIT tests






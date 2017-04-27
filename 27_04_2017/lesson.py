class A:
    def f(self):
        return 42

class Length:
    def __set__(self, obj, value):
        obj._l = 10 * value
    def __get__(self, obj, objtype):
        return obj._l / 10

class Line:
    l = Length()

    def __init__(self):
        self._l = 0

class Volume:
    def __get__(self, obj, objtype):
        return obj._l * obj._w * obj._h

class Box:
    def __init__(self, h, w, l):
        self._h, self._w, self._l = h, w, l
    volume = Volume()


class Linee:

    def __init__(self):
        self._l = 0

    @property
    def l(self):
        return self._l / 9

    @l.setter
    def l(self, value):
        self._l = 9 * value


class Boxe:

    def __init__(self, l, w, h):
        self._l, self._w, self._h = l, w, h

    @property
    def volume(self):
        return self._l * self._w * self._h


### Создание метакласса

class Meta(type):

    def __new__(cls, name, parents, props):
        new_props = {}
        for name, value in props.items():
            if not name.startswith('unused_'):
                new_props[name] = value
        return super().__new__(cls, name, parents, new_props)


class Metaa(type):

    def __call__(*args, **kwargs):
        instance = type.__call__(*args, **kwargs)
        instance.a = 1
        return instance

class Metaaa(type):

    def __call__(*args, **kwargs):
        print('Call')
        return type.__call__(*args, **kwargs)

    def __new__(*args, **kwargs):
        print('New')
        return type.__new__(*args, **kwargs)

    def __init__(*args, **kwargs):
        print('Init')
        type.__init__(*args, **kwargs)


class MMeta(type):

    def __new__(cls, name, parents, props):
        new_cls = super().__new__(cls, name, parents, props)
        if hasattr(cls, 'children'):
            cls.children[name] = new_cls
        else:
            cls.children = {}
        return new_cls


import abc

class Aa(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def f(self):
        pass
    @abc.abstractclassmethod
    def g(self):
        pass
    @abc.abstractclassmethod
    def h(self):
        pass

if __name__ == '__main__':

    # a = A()
    # print(a.f)
    # print(A.f)

    # a = Line()
    # a.l = 10
    # print(a.l)
    # print(a._l)

    # b = Box(10, 20, 30)
    # print(b.volume)
    # print(b._l)
    # b._l = 40
    # print(b.volume)

    # l = Linee()
    # l.l = 10
    # print(l._l)
    #
    # b = Boxe(10, 20, 30)
    # print(b.volume)
    # b.volume = 10   Потому что нет своего сеттера в проперти, пока мы его не определим через setter

    # import pprint
    # class A(metaclass=Meta):
    #     a = 1
    #     unused_a = 1
    #
    # pprint.pprint(dir(A)
    # class A(metaclass=Metaa):
    #     pass
    #
    # a = A()
    # print(a.a)
    # print(vars(a))

    # class A(metaclass=Metaaa): ## Вызывается метод NEW and INIT
    #     pass
    #
    # a = A()  ## Вызоветься метод Call

    # class A(metaclass=MMeta):
    #     pass
    #
    # class B(A):
    #     pass
    #
    # print(A.children)
    #
    # class C(B):
    #     pass
    #
    # print(A.children)

    class B(Aa):
        def g(self):
            pass

        def f(self):
            pass

        def h(self):
            pass


    import weakref

    class D:
        pass
    d = D()
    import sys
    print(sys.getrefcount(d))

    c = weakref.ref(d)

    print(sys.getrefcount(d))
    print(c())



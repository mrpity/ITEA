
import pprint
import sys


def decor(any_func):
    def wrapper():
        print('AOE or')
        test = any_func()
        print('or India')
        return test
    return wrapper

def wrapper():
    print('AOE or')
    test1 = echo_func()
    return test1

# @decor
def echo_func():
    print('Egypt')
    return 'zopa'


if __name__ == '__main__':
    # echo_func()

    def test():
        c = 1
        while True:
            yield c
            c += 1

    print(test().__next__())
    print(test().__next__())

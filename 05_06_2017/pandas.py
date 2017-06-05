import numpy as np


def p_decor(f):
    def wrapper():
        print(f)
    return wrapper



if __name__ == '__main__':


    a = np.zeros(10)
    print(a)
    print(type(a))
    print(a.shape)
    print(np.ones((2,5)))


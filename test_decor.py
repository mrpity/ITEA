
def decor(f):
    def wrapper():
        print('----')
        f()
        print('---')
    return wrapper

@decor
def f():
    print("test")

f()
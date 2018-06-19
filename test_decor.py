
# def decor(f):
#     def wrapper():
#         print('----')
#         f()
#         print('---')
#     return wrapper
#
# #@decor
# def f():
#     print("test")
#
# z = decor(f)()



print("123")

def test():
    for x in range(0, 10):
        print(x)
        line = yield
        print(line)
        continue

gen = test()
gen.__next__()
gen.send('sda')



import collections

def f():
    return 5


class Maxer(collections.UserList):
    def max(self):
        self.data.append(f())
        return max(self.data)

    
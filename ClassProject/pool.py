import random
import math

class Pool:
    def __init__(self, w, l, b_f, s_f):
        self._w, self._l = w, l
        self._fishes = self._create_fishes(BigFish, b_f) + \
                      self._create_fishes(SmallFish, s_f)

    def _create_fishes(self,cls, qty):
        return [cls(
            random.randint(1, self._w),
            random.randint(1, self._l),
            self
        ) for _ in range(qty)]

    def __repr__(self):
        return '\n'.join([str(fish) for fish in self._fishes])

    def move_fishes(self):
        for fish in self._fishes:
            fish.move()

    def get_width(self):
        return self._w

    def get_length(self):
        return self._l

    def get_nearest_small_fishes(self, x, y):
        return min([fish for fish in self._fishes if isinstance(fish, Eatable)],
            key=lambda _: _.get_distance(x,y))

class Fish:
    def __init__(self, x, y, pool):
        self._x, self._y = x, y
        self._pool = pool


    def get_distance(self, x, y):
        return math.hypot(self._x - x, self._y - y)


    def move(self):
        self._x = 1 if self._x < 1 else self._x
        self._x = self._pool.get_width() if self._x > self._pool.get_width()\
            else self._x
        self._y = 1 if self._y < 1 else self._y
        self._y = self._pool.get_length() if self._y > self._pool.get_length()\
            else self._y

    def __repr__(self):
        return "{}(x={}, y={})".format(
            self.__class__.__name__,
            self._x,
            self._y
        )


class Eatable:
    pass

class SmallFish(Fish, Eatable):
    def __init__(self, x, y, pool: Pool):  ### pool: Pool --- type anotations
        super().__init__(x, y, pool)


    def move(self):
        self._x = self._x + random.randint(-1, 1)
        self._y = self._y + random.randint(-1, 1)
        super().move()

class BigFish(Fish):
    def __init__(self, x, y, pool):
        super().__init__(x, y, pool)

    def move(self):
        nearest_fish = self._pool.get_nearest_small_fishes(self._x, self._y)
        self._x += - 2 if self._x > nearest_fish._x else 2
        self._y += -2 if self._y > nearest_fish._y else 2
        super().move()

if __name__ == '__main__':
    p = Pool(10, 10, 3, 5)
    print(p)
    p.move_fishes()
    print('--------------')
    print(p)


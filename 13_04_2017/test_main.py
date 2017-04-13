import unittest
import unittest.mock
import main
import sys

print(sys.path)

class TestMain(unittest.TestCase):

    def setUp(self):
        m = main.Maxer([1, 2, 3])
        print('Set Up')

    @unittest.mock.patch('main.f')
    def testMax1(self, a):
        print(a)
        a.side_effect = [0]   ## значения из этого списка будут возвращаться когда функция будет вызываться
        self.assertEqual(self.m.max(), 3, 'max(1,2,3)')
        print(self.m)

    def testMax2(self):
        m.append(5)
        self.assertEqual(self.m.max(), 5)

    def tearDown(self):
        print('Tear Down')
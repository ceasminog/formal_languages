import unittest
from main import find_shortest_string
import math

class  Testfind_shortest_string(unittest.TestCase):
    def test1(self):
        with self.assertRaises(ValueError): find_shortest_string('ab + c.', 'a', 6, 5)

    def test2(self):
        with self.assertRaises(ValueError): find_shortest_string('ab + c.', 'a', 'y')

    def test3(self):
        with self.assertRaises(ValueError): find_shortest_string('ab + c.', 9, 8)

    def test4(self):
        with self.assertRaises(ValueError): find_shortest_string('ab+c.', 'asxdf', 2)

    def test_ans1(self):
        self.assertEqual(find_shortest_string(list("ab+c."), 'a', 1), 1)

    def test_ans2(self):
        self.assertEqual(find_shortest_string(list("ab.c+"), 'c', 1), 1)

    def test_ans3(self):
        self.assertEqual(find_shortest_string(list("ab.c+"), 'c', 2), math.inf)

    def test_ans3(self):
        self.assertEqual(find_shortest_string(list("a1.1.aa.+"), 'a', 4), math.inf )


if __name__ == '__main__':
    unittest.main()

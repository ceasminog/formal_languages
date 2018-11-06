import unittest
from main import find_shortest_string


class test_find_shortest_string(unittest.TestCase):
    def test_types(self):
        with self.assertRaises(TypeError):
            find_shortest_string('1ggg.gg', 'a', 6)
        with self.assertRaises(TypeError):
            find_shortest_string('ab + c.', 'a', 6, 5)
        with self.assertRaises(TypeError):
            find_shortest_string('ab + c.', 'a', 'y')
        with self.assertRaises(TypeError):
            find_shortest_string('ab + c.', 9, 8)
        with self.assertRaises(TypeError):
            find_shortest_string('ab + c.', 'asxdf', 2)

    def test_ans(self):
        self.assertEqual(find_shortest_string('ab + c.', 'a', 1), 2)


if __name__ == '__main__':
    unittest.main()

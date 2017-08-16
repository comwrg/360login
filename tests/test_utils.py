import unittest

from _360login.utils import *


class TestUtils(unittest.TestCase):
    def test_md5(self):
        self.assertEqual(md5('good luck'), 'ab4c946c01be2a78a27940ef9faa9471')


if __name__ == '__main__':
    unittest.main()

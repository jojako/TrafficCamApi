import unittest
from main import *


class UnitTest(unittest.TestCase):
    def test1(self):
        self.test_url = ApiCon("http://www.test.com")
        self.assertEqual(self.test_url.api_url, "http://www.test.com")

    def test2(self):
        self.test_error_mess = ErrorWindow("Error message")
        self.assertEqual(self.test_error_mess.error_input, "Error message")

    def test3(self):
        self.

    def test4(self):
        pass
    def test5(self):
        pass

if __name__ == '__main__':
    unittest.main()

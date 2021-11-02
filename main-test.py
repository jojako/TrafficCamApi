import unittest
from main import *
import os


class UnitTest(unittest.TestCase):
    def test1(self):
        self.test_url = ApiCon("http://www.test.com")
        self.assertEqual(self.test_url.api_url, "http://www.test.com")

    def test2(self):
        self.test_error_mess = ErrorWindow("Error message")
        self.assertEqual(self.test_error_mess.error_input, "Error message")

    def test3(self):
        self.test_write = ApiWindow.write_to_file(self, "Test")
        try:
            f = open('api.txt')
            f.close()
            os.remove('api.txt')
        except:
            pass

    def test4(self):
        self.apitestw = ApiWindow(True)
        self.assertTrue(self.apitestw.main_opened)

    def test5(self):
        self.test_url = ApiCon("http://www.api.com")
        self.assertEqual(self.test_url.api_url, "http://www.api.com")

if __name__ == '__main__':
    unittest.main()

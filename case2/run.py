#coding=utf-8
import unittest
import os
import HTMLTestRunner


class RunCase(unittest.TestCase):
    def test_all_case(self):
        file_path = os.path.join(os.getcwd() + "/report/" + "all_case.html")
        f = open(file_path, 'wb')
        case_path = os.path.join(os.getcwd(), 'case')
        suite = unittest.defaultTestLoader.discover(case_path, '*case.py')
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=f, title="全量测试报告", verbosity=2)
        runner.run(suite)


if __name__ == '__main__':
    unittest.main()

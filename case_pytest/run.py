#coding=utf-8
import pytest
import os


class RunCase():
    def test_part_case(self):
        case_path = os.path.join(os.getcwd(), 'case_pytest')
        pytest.main([
            "-s", "-v", "-q", "--html=reportname01.html",
            case_path + "\\test_001_login_case.py::TestLoginCase",
            case_path + "\\test_002_shenl_case.py::TestShenlCase"
        ])
        pytest.main([
            "-s", "-v", "-q", "--lf", "--html=reportname02.html",
            case_path + "\\test_001_login_case.py::TestLoginCase",
            case_path + "\\test_002_shenl_case.py::TestShenlCase"
        ])

    def test_all_case(self):
        case_path = os.path.join(os.getcwd(), 'case_pytest')
        pytest.main([
            "-s", "-v", "-q",
            "--html=C:\\ZL_testing\\report_path\\reportname01.html", case_path
        ])
        pytest.main([
            "-s", "-v", "-q", "--lf",
            "--html=C:\\ZL_testing\\report_path\\reportname02.html", case_path
        ])


if __name__ == '__main__':
    a = RunCase()
    a.test_all_case()

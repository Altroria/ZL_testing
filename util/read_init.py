#coding=utf-8
import os
import configparser


class ReadIni(object):
    def __init__(self, database_path=None):
        if database_path == None:
            self.database_path = "LocalElement.ini"
        else:
            self.database_path = database_path
        self.data = self.load_ini()

    def load_ini(self):
        cf = configparser.ConfigParser()
        #file_path = "C:\Automated_testing\ZL_testing\config\LocalElement.ini"
        file_path = os.path.join(os.getcwd() + "/config/" + self.database_path)
        cf.read(file_path, encoding='utf-8-sig')
        return cf

    def get_value(self, by, key):
        return self.data.get(by, key)


if __name__ == "__main__":
    a = ReadIni()
    print(a.get_value("iframe", "iframe1"))

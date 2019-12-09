#coding=utf-8
import os
import xlrd
import datetime
from xlutils.copy import copy


class ExcelUtil(object):
    def __init__(self, excel_path=None, index=None):
        if excel_path == None:
            excel_path = os.path.join(
                os.getcwd()) + "/config/" + "casedata.xlsx"
        if index == None:
            index = 0
        self.data = xlrd.open_workbook(excel_path)
        self.table = self.data.sheets()[index]

    #获取excel数据
    def get_data(self):
        result = []
        rows = self.get_lines()
        if rows != None:
            for i in range(rows):
                col = self.table.row_values(i)
                result.append(col)
            return result
        else:
            return None

    #获取行数
    def get_lines(self):
        rows = self.table.nrows
        if rows >= 1:
            return rows
        else:
            return None

    #获取单元格数据
    def get_col_value(self, row, col):
        if self.get_lines() > row:
            if self.table.cell(row, col).ctype == 3:
                date = self.table.cell(row, col).value
                value = datetime.date.fromtimestamp(date)
            else:
                value = self.table.cell(row, col).value
            return value
        else:
            return None

    #写入数据
    def write_value(self, row, value):
        read_value = self.data
        write_data = copy(read_value)
        write_data.get_sheet(0).write(row, 7, value)
        write_data.save(
            os.path.join(os.getcwd()) + "/config/" + "keyword.xlsx")


if __name__ == "__main__":
    ex = ExcelUtil("C:\\Users\\sunH\\Desktop\\待提交_20191206.xls")
    print(ex.get_data())

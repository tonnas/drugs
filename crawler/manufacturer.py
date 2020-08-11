import xlrd
from os import path
from base import BaseClass
from datetime import datetime


class Manufacturer(BaseClass):

    def __init__(self):
        super().__init__()
        self.file_name = path.abspath(path.join(__file__, '../../data/manufacturer.xls'))

    def run(self):
        self.read_data_from_file()

    def read_data_from_file(self):
        workbook = None
        try:
            workbook = xlrd.open_workbook(self.file_name, formatting_info=True)
        except FileNotFoundError as fe:
            print('File Not found: {}'.format(self.file_name))
        except Exception as e:
            print('File Error: {}'.format(repr(e)))

        if workbook:
            sheet = workbook.sheet_by_index(0)
            for y in range(sheet.nrows):  # y for rows
                cell_code = sheet.cell_value(y, 0).strip()
                cell_name = sheet.cell_value(y, 1).strip()
                if len(cell_code) == 3 and cell_name:
                    doc = {
                        'code': cell_code,
                        'name': cell_name,
                        'checked_at': datetime.now(),
                        'source': 'health.gov.sk'
                    }
                    self.mongo.manufacturer.update({'code': doc['code']}, doc, True)

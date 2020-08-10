import xlrd
from os import path
from base import BaseClass
from datetime import datetime


class Shortcut(BaseClass):

    def __init__(self):
        super().__init__()
        self.file_name = path.abspath(path.join(__file__, '../../data/shortcuts.xls'))

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
            group = {}
            for y in range(sheet.nrows):  # y for rows
                cell_code = sheet.cell_value(y, 0)
                cell_name = sheet.cell_value(y, 1)

                if cell_code and cell_name:
                    doc = {
                        'shortcut': cell_code,
                        'text': cell_name,
                        'checked_at': datetime.now()
                    }
                    self.mongo.shortcut.update({'shortcut': doc['shortcut']}, doc, True)

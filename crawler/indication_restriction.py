# -*- coding: utf-8 -*-

from base import BaseClass
from os import path


class IndicationRestrictionRTF(BaseClass):
    FIE = None

    def __init__(self):
        super().__init__()
        self.file_name = path.abspath(path.join(__file__, '../../data/restrictions.txt'))

    def run(self):
        self.read_data_from_file()

    def read_data_from_file(self):
        lines = None
        try:
            with open(self.file_name) as file_in:
                lines = []
                for line in file_in:
                    lines.append(line)
        except FileNotFoundError as fe:
            print('File Not found: {}'.format(self.file_name))
        except Exception as e:
            print('File Error: {}'.format(repr(e)))

        i = 0
        for line in lines:
            i = i + 1
            # if i <= 8:
            #     continue
            #
            # pprint(line.strip())
            # if i > 20:
            #     break

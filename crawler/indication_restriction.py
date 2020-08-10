# -*- coding: utf-8 -*-

from base import BaseClass
from pprint import pprint
from os import path
import PyPDF2


class IndicationRestrictionRTF(BaseClass):
    FIE = None

    def __init__(self):
        super().__init__()
        self.file_name = path.abspath(path.join(__file__, '../../data/restrictions.pdf'))

    def run(self):
        self.read_data_from_file()

    def read_data_from_file(self):
        pdfFileObj = None
        try:
            pdfFileObj = open(self.file_name, 'rb')
        except FileNotFoundError as fe:
            print('File Not found: {}'.format(self.file_name))
        except Exception as e:
            print('File Error: {}'.format(repr(e)))

        if pdfFileObj:
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            print(pdfReader.numPages)
            pageObj = pdfReader.getPage(0)
            print(pageObj.extractText().encode('utf-8', "replace").encode('ascii'))
            pdfFileObj.close()

import xlrd
import requests
import unidecode
from os import path
from pprint import pprint
from base import BaseClass
from datetime import datetime


class CategorizedDrugsCrawler(BaseClass):
    CONDITIONAL = 'Podmienena'
    TEMPORARY = 'Docasna'
    UHR_SPEC = 'UhrSpec'
    CONDITIONAL_CATEGORY = 'PodmienenaKategora'
    TEMPORARY_CATEGORY = 'DocasnaKategora'
    UHR_SPEC_CATEGORY = 'UhrSpecSkupina'

    def __init__(self):
        super().__init__()
        self.file_name = path.abspath(path.join(__file__, '../../data/development_data.xls'))

    def run(self):
        pprint('Starting script Sir!')
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
            headers1 = {}
            headers2 = {}
            conditional = None
            temporary = None
            uhr_spec = None
            indication_restriction_id = None
            for y in range(sheet.nrows):  # y for rows
                drug_doc = {}
                indication_restriction_doc = {}
                row_type = None
                for x in range(sheet.ncols):  # x for columns
                    cell_value = sheet.cell_value(y, x)
                    if y == 0:  # first row
                        cc_cell_value = self.camel_case(cell_value)
                        if cc_cell_value == self.CONDITIONAL:
                            conditional = x
                            cc_cell_value = ''
                        if cc_cell_value == self.TEMPORARY:
                            temporary = x
                            cc_cell_value = ''
                        if cc_cell_value == self.UHR_SPEC:
                            uhr_spec = x
                            cc_cell_value = ''

                        headers1[x] = cc_cell_value
                        continue
                    if y == 1:  # second row
                        cc_cell_value = self.camel_case(cell_value)
                        if x == conditional:
                            cc_cell_value = self.CONDITIONAL_CATEGORY
                        if x == temporary:
                            cc_cell_value = self.TEMPORARY_CATEGORY
                        if x == uhr_spec:
                            cc_cell_value = self.UHR_SPEC_CATEGORY

                        headers2[x] = cc_cell_value if cc_cell_value else headers1[x]
                        continue

                    fmt = workbook.xf_list[sheet.cell_xf_index(y, x)]
                    font = workbook.font_list[fmt.font_index]
                    if cell_value:
                        if font.bold == 1:
                            row_type = 'ir'
                            indication_restriction_doc[headers1[x]] = str(cell_value)
                        else:
                            row_type = 'd'
                            drug_doc[headers2[x]] = str(cell_value)
                    # columns end

                if not row_type:
                    continue

                if row_type == 'ir':
                    indication_restriction_id = self.get_ir_id(indication_restriction_doc)
                    continue

                if row_type == 'd':
                    drug_doc['indication_restriction_id'] = indication_restriction_id
                    drug_doc['checked_at'] = datetime.now()
                    self.mongo.drugs.update({'Kod': drug_doc['Kod']}, drug_doc, True)

    def get_ir_id(self, doc):
        ir_doc = self.mongo.indication_restriction.find_one(doc)
        if ir_doc and '_id' in ir_doc:
            return ir_doc['_id']

        doc['created_at'] = datetime.now()
        ir_doc = self.mongo.indication_restriction.insert_one(doc)
        return ir_doc.inserted_id

    @staticmethod
    def camel_case(cell_value):
        cell_value = unidecode.unidecode(cell_value.replace('%', 'PERCENT'))
        return ''.join(e for e in cell_value if e.isalnum())

    @staticmethod
    def download_data_file(fileName):
        if not path.exists(fileName):
            dls = "https://www.health.gov.sk/" \
                  "Zdroje?/Sources/kategorizacia/zkl/202005/lieky/cast_A_zoznam_liekov_k_01_05_2020.xls"
            resp = requests.get(dls)
            output = open(fileName, 'wb')
            output.write(resp.content)
            output.close()
        else:
            print("File is already saved..")
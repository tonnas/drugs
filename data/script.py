
# Download file 
# pip install requests
import requests
from os import path
import xlrd
import re
import unidecode

fileName = 'new_data.xls'


def camelCase(s):
	s = unidecode.unidecode(s)
	s = ''.join(e for e in s if e.isalnum())
	return s

def readDataFile(fileName):
	book = xlrd.open_workbook(fileName, formatting_info=True)
	sheet = book.sheet_by_index(0)

	print(sheet.nrows)
	print(sheet.ncols)

	headers1 = []
	headers2 = []
	documents = []
	podmienenaCategory = 0
	docasnaCategory = 0
	uhrSpecSkupina = 0
	for y in range(sheet.nrows): # y for rows
		for x in range(sheet.ncols): # x for columns
			cellValue = sheet.cell_value(y, x)
			if y == 0:
				camelCaseCellValue = camelCase(cellValue)
				if camelCaseCellValue == 'Podmienena':
					podmienena = x
					camelCaseCellValue = ''
				if camelCaseCellValue == 'Docasna':
					docasna = x
					camelCaseCellValue = ''
				if camelCaseCellValue == 'UhrSpec':
					uhrSpecSkupina = x
					camelCaseCellValue = ''
				headers1.append(camelCaseCellValue)
				continue
			if y == 1:
				camelCaseCellValue = camelCase(cellValue)
				if x == podmienena:
					camelCaseCellValue = 'PodmienenaKategora'
				if x == docasna:
					camelCaseCellValue = 'DocasnaKategora'
				if x == uhrSpecSkupina:
					camelCaseCellValue = 'UhrSpecSkupina'

				headers2.append(camelCaseCellValue)
				continue

			fmt = book.xf_list[sheet.cell_xf_index(y, x)]
			font = book.font_list[fmt.font_index]
			if cellValue:
				if font.bold == 1:
					print(headers1[x] + ' => ' + str(cellValue))
				else:
					print(headers2[x] + ' => ' + str(cellValue))

		if y >= 3:
			break

	print()
	print('It`s done Lord..')


def downloadDataFile(fileName):
	if not path.exists(fileName):
		dls = "https://www.health.gov.sk/Zdroje?/Sources/kategorizacia/zkl/202005/lieky/cast_A_zoznam_liekov_k_01_05_2020.xls"
		resp = requests.get(dls)

		output = open(fileName, 'wb')
		output.write(resp.content)
		output.close()
	else:
		print("File is already saved..")


# downloadDataFile(fileName)
readDataFile(fileName)


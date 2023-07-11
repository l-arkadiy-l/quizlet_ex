import pandas as pd
import openpyxl
import openpyxl as ox
from translator import *

file_errors_location = r'1000 most used english words.xlsx'
df = pd.read_excel(file_errors_location, index_col=None)
df["B"] = ""
df["C"] = ""
# print(df[df.columns[1]].values[600], str(df[df.columns[1]].values[200]) == 'nan')
words = {i + 1: df.values[i].tolist()[0] for i in range(len(df.values)) if (str(df[df.columns[1]].values[i]) in ['nan', ''])}
w_20 = 10
print(words)
# get_translate(list(words.values())[:w_20])
srcfile = openpyxl.load_workbook(file_errors_location)
sheet_name = srcfile.sheetnames[0]
sheetname = srcfile[sheet_name]
sheet = srcfile.worksheets[0]
sheet.insert_cols(2)
srcfile.save('my.xlsx')
for i in list(words.keys())[:w_20]:
    # print(i)
    sheetname[f'C{i}'] = 1
for i in range(1, int(list(words.keys())[-1])):
    sheetname[f'C{i}'] = f'=ЕСЛИ(B{i}<>1;A{i};)'
srcfile.save('new.xls')
df = pd.read_excel('new.xls', header=None)
df.to_excel(file_errors_location, index=False, header=False)
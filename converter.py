#The MIT License (MIT)
#
#Copyright (c) 2016 anooptoffy
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import xlrd
import xlwt
import os
from os.path import abspath
import sys




def open_file(path):
    """
    Open and read an Excel file
    """
    # Open the workbook
    xl_workbook = xlrd.open_workbook(path)
    
    # List sheet names, and pull a sheet by name
    #
    sheet_names = xl_workbook.sheet_names()
    print('Sheet Names', sheet_names)
    
    xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
    
    # Or grab the first sheet by index 
    #  (sheets are zero-indexed)
    #
    xl_sheet = xl_workbook.sheet_by_index(0)
    print ('Sheet name: %s' % xl_sheet.name)
    
    # Pull the first row by index
    #  (rows/columns are also zero-indexed)
    #
    row = xl_sheet.row(0)  # 1st row
    
    # Print 1st row values and types
    #
    from xlrd.sheet import ctype_text   
    
    print('(Column #) type:value')
    for idx, cell_obj in enumerate(row):
        cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
        print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
    
    # Print all values, iterating through rows and columns
    #
    num_cols = xl_sheet.ncols   # Number of columns
    for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
        print ('-'*40)
        print ('Row: %s' % row_idx)   # Print row number
        for col_idx in range(0, num_cols):  # Iterate through columns
            cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            print ('Column: [%s] cell_obj: [%s]' % (col_idx, cell_obj))
                               
                                
#----------------------------------------------------------------------
if __name__ == "__main__":
    f_path = abspath("demo.xlsx")
    open_file(f_path)                                
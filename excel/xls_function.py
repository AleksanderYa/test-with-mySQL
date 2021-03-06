import xlrd
import re
import os

def connect(func):
    def wrapper(*arg, **kwarg):
        try:
            arge = arg[0]
            if type(arge) == str:
                rb = xlrd.open_workbook(arge, formatting_info=True)
                sheet = rb.sheet_by_index(0)
                print('Connection succerfull')
                print()
                res = func(sheet,*arg, **kwarg)
                return res
            else:
                print('wrong format text to connect')
        except Exception as e:
            print('connect',e) 
    return wrapper



@connect
def waybill(sheet, text):
    coll = ''
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        for c_ell in row:
            try:
                if c_ell:
                    reg_text = r'Видаткова накладна'
                    res = re.findall(reg_text, c_ell)
#                     res = c_ell.startswitch('Видаткова накладна')
                    if res and not coll:
                        coll = c_ell
#                         print(coll)
                        return c_ell
            except Exception as e:
                pass
#     return waybill_text(text)
        
@connect
def bayer(sheet, text):
    col = ''
    col2 = ''
#     print(type(sheet))
    for rownum in range(sheet.nrows):
        finded_text = r'Покупець:'
        row = sheet.row_values(rownum)
        for c_el in row:
            try:
                if c_el:
                    res = re.match(finded_text, c_el)
                    if res and not col:
                        col = c_el
                    elif col and c_el and not col2:
#                         print(c_el)
                        col2 = c_el
                        return c_el           
            except Exception as e:
                pass
#


            
@connect
def product(sheet, text):
    coll = ''
    base = []
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        for c_ell in row:
                if c_ell:
                    c_ell = str(c_ell)
                    
                    try:
                        reg_text = r'Сума без ПДВ'
                        reg_end_text = r'Всього:'
                        res = re.match(reg_text, c_ell)
                        res_end = re.search(reg_end_text, c_ell)
                        if res and not coll:
                            coll = c_ell

                        elif coll and not res_end:
                            c_ell = str_to_float(c_ell)
                            base.append(c_ell)
                            
                        elif res_end and coll:
                            coll = ''
                            base = test_sorted(base)
                            return base

                    except Exception as e:
                        print('in try', e)


def str_to_float(text):
    try:
        return float(text)
    except Exception as e:
        return text

    
def test_sorted(obj):
    base = []
    re_base = []
    col = 5
    col_pos = len(obj)/6
#     obj.append('None')
    if col_pos == abs(col_pos):
        try:
            for i in obj:       
                if col:
#                     print('ts if',i, col)
                    re_base.append(i)
                    col -= 1
                elif not col:
#                     print('ts else',i, col)
                    re_base.append(i)
                    base.append(re_base)
                    re_base = []
                    col = 5
            print('all done.....base-list of product create')
            print()
            return base
        except Exception as e:
            print('test_sorted',e)
        
        
def add_bayway(product_list, *arg):
    try:
        if type(product_list) == list: 
            product = product_list[::-1]
            temp = []
            temp.append(arg[0])
            temp.append(arg[1])
            product.append(temp)
            product = product[::-1]
            print('All done...bayer and waybill add to list')
            print()
            return product
    except Exception as e: 
        print(e) 
        print('Wrong format in add_bauway')
        print(arg[0])
        return arg[0] 

def create_infolist(text):
    return add_bayway(
        product(text),
        bayer(text),
        waybill(text)
    )
   
    
def search_xls():
    temp_list = []
    for i in os.walk('./'):
        for ii in i[2]:
            if ii.endswith(".xls") and i[0] == './' and test_to_waybill(ii):
                res = ii
#                 res = test(ii)
                print('Finded file -->',ii)
                temp_list.append(res)
                print(res)
                print()
            elif ii.endswith(".xls") and i[0] != './' and test_to_waybill(ii):
#                 res = test(ii)
                res = i[0]+ '/' + ii
                print('Finded file -->',ii)
                temp_list.append(res)
                print(res)
                print()
    return temp_list
 
def test_to_waybill(text):
    str.startswith
    if text.startswith('Видаткова'):
         return True
    else:
        return False
    
def waybill_text(text):
    temp_list = []
#     res = ''
    res = text.split(' ')
    print('waybill_text res', res)
    date = res[-1]
    print('waybill_text datwe', date)
    date = date.split('.')
    print('waybill_text date', date)
    dat = date[0]+'/'+date[1]+'/'+date[2]
    print(dat)
    temp_list.extend([res[0], res[3], dat])
    print(temp_list)
    return temp_list

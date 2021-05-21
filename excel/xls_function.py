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
#     try:
    coll = ''
    base = []
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        for c_ell in row:
#                 try:
#                     print(c_ell)
                if c_ell:
                    c_ell = str(c_ell)
#                         print(c_ell)
                    try:
                        reg_text = r'Сума без ПДВ'
                        reg_end_text = r'Всього:'
                        res = re.match(reg_text, c_ell)
                        res_end = re.search(reg_end_text, c_ell)
    #                             print(res, '----------', coll)
                        if res and not coll:
    #                                 print('1',c_ell)
                            coll = c_ell
    #                                 base.append(c_ell)

                        elif coll and not res_end:
                            c_ell = str_to_float(c_ell)
                            base.append(c_ell)
    #                                 print('2',c_ell)
                        elif res_end and coll:
                            coll = ''
    #                                 print('3',c_ell)
                            base = test_sorted(base)
                            return base
    #                             else:
    #                                 base.append("lol")
                    except Exception as e:
                        print('in try', e)

#     return base               
#     except Exception as e:
#         print(e)
        

    
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

 
# def search_xls():
#     temp_list = []
#     for i in os.walk('./'):
#         for ii in i[2]:
#             if ii.endswith(".xls") and i[0] == './' :
#                 res = ii
#                 print('Finded file -->',ii)
#                 temp_list.append(res)
#                 print(res)
#                 print()
#             elif ii.endswith(".xls") and i[0] != './' :
#                 res = i[0]+ '/' + ii
#                 print('Finded file -->',ii)
#                 temp_list.append(res)
#                 print(res)
#                 print()
#     return temp_list
 
    
    
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
    try:
        pattern_nak = 'Видаткова'
        pattern_nomber = r'[№] [0-9]+|[№][0-9]+|[№]\s+[0-9]+'
        pattern_date = r'[0-9]{2}[.]{1}[0-9]{2}[.]{1}[0-9]+'
        res_nomber = re.findall(pattern_nomber, text)[0][1:]
        res_date = re.findall(pattern_date, text)[0]
        res_nak = re.findall(pattern_nak, text)[0]

        return [res_nak, res_nomber, res_date]
    except Exception as e:
        print(e)
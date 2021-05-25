import xlrd
import re
import os

'''
Название компании           base[0][0]
Полное название документа   base[0][1][0]
Тип документа               base[0][1][1]
Номер документа             base[0][1][2] 
Дата документа              base[0][1][3]

Список товара               base[1]

Пози  номер в накладной     base[1][n][0]
Название товара             base[1][n][1]
Количество  товара          base[1][n][2]
Наименование веса           base[1][n][3]
Цена единицу веса           base[1][n][4]
Цена за товар               base[1][n][5]

'''

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
                        col2 = c_el
#                         print(c_el)

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
                            coll = c_ell   
#                                 print('1',c_ell)
                        elif coll and not res_end:
                            c_ell = str_to_float(c_ell)
                            base.append(c_ell)
    #                                 print('2',c_ell)
                        elif res_end and coll:
                            coll = ''
                            base = test_sorted(base)
#                                 print('3',c_ell)

                            return base

                    except Exception as e:
                        print('in try', e)

            
            
            
            
    
def create_infolist(way,name):
    '''
    input str путь к файлу
    
    '''
    return add_bayway(
        product(way),
        bayer(way),
        waybill_text(name)
    )

    

    
    
def add_bayway(product_list, *arg):
    try:
        if type(product_list) == list: 
            product = []
            product.append(product_list[::])
            temp = []
            temp.append(arg[0])
            print(arg[0])
            temp.append(arg[1])
            print(arg[1])
            product.append(temp)
            product = product[::-1]
            print('All done...bayer and waybill add to list')
            print()
            
            return product
        
    except Exception as e: 
        print(e) 
        print('Wrong format in add_bauway')
        print(arg[0])
        
        return e 

    

    
    
    
    
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
        

        
        
        
        

def waybill_text(text):
    try:
        text[1]
        pattern_nak = 'Видаткова'
        pattern_nomber = r'[№] [0-9]+|[№][0-9]+|[№]\s+[0-9]+'
        pattern_nomber_end = r'[0-9]+'
        pattern_date = r'[0-9]{2}[.]{1}[0-9]{2}[.]{1}[0-9]+'
        res_nomber = re.findall(pattern_nomber, text)[0]
        res_nomber_end = re.findall(pattern_nomber_end, text)[0]
        res_date = re.findall(pattern_date, text)[0]
        res_nak = re.findall(pattern_nak, text)[0]
        print('watet', [res_nak, res_nomber_end, res_date])
        
        return [text, res_nak, res_nomber_end, res_date]
    
    except Exception as e:
        print(e)
        

 
    
    
    
    
def search_xls():
    temp_list = []
    for i in os.walk('./'): # Гуляем по кореневой папке и всем вложениям, класная штука, возвращает список
        
        for ii in i[2]: # берем название папки или файла из списка
            
            if ii.endswith(".xls") and i[0] == './' and test_to_waybill(ii):  # если ексель файл то в +
                print('Finded file -->',ii)
                temp_list.extend([[ii, waybill_text(ii)]])
                print(ii)
                print()
            elif ii.endswith(".xls") and i[0] != './' and test_to_waybill(ii):
                res = i[0]+ '/' + ii
                print('Finded file -->',ii)
                temp_list.extend([[res, waybill_text(ii)]])
                print(res)
                print()
                
    return temp_list
 
   

    
    
def test_to_waybill(text):
    str.startswith
    if text.startswith('Видаткова'):
         return True
        
    else:
        return False
    
    
def correct_weight(base):
    base = base
    for i in base:
        for ii in i[1]:
#             print(ii[3])
            if ii[3] == 'кг':
                ii[3] = 'т'
                ii[2] = ii[2]/1000
                ii[4] = ii[4]*1000
                print('correct кг to t')
    return base


# def correct_price(base):
#     base = base
#     for i in base:
#         for ii in i[1]:
# #             print(ii[3])
# #             if ii[4] == 'кг':
#             ii[4] = ii[4]*1.2
#             ii[5] = ii[5]*1.2
#             print('correct price to pdv')
#     return base
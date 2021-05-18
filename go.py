import pymysql

def connected(func):
    def wrapper(*arg, **kwarg):
        try:
            connect = pymysql.connect(
                host='localhost',
                user='root',
                password='37112202',
                database='test_db'
            )
            print('*'*38)
            print('Connection to base test_db succerfull!')
            print('*'*38)
            func(connect, *arg, **kwarg)
        except Exception as e:
            print('*'*38)
            print(e)
            print('*'*38)
    return wrapper

# Проіерить версию
@connected
def version_db(connect):
    with connect:
        cur = connect.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()
        print("Database version: {}".format(version[0]))
        print('*'*38)
        
        
# Прочитать с бази
@connected
def work_with_base(connect, query_text, commit=False):
    
    '''
    Функция отправляет запрос на SQL сервер,
    query_text - текс запроса
    commit - булевое значение по факту False, когда тру делается комит, который нужен, для записи и \
    обновления обновления данных
    '''
    
    with connect:
        cur = connect.cursor()
        cur.execute(query_text)
        if commit:
            connect.commit()
            print("Commit done")
            print('*'*38)
        print("Query done")
        print('*'*38)
import mysql.connector
import pswrd
star = 48

'''
#  CREATE Database
```
CREATE DATABASE databasename; 

DROP DATABASE databasename; 
```
####  CREATE TABLE Statement

```
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    column3 datatype,
   ....
); 
 
CREATE TABLE new_table_name AS
    SELECT column1, column2,...
    FROM existing_table_name
    WHERE ....; 
```    
    NOT NULL - Ensures that a column cannot have a NULL value
    UNIQUE - Ensures that all values in a column are different
    PRIMARY KEY - A combination of a NOT NULL and UNIQUE. Uniquely identifies each row in a table
    FOREIGN KEY - Prevents actions that would destroy links between tables
    CHECK - Ensures that the values in a column satisfies a specific condition
    DEFAULT - Sets a default value for a column if no value is specified
    CREATE INDEX - Used to create and retrieve data from the database very quickly

####  DROP TABLE Statement
    DROP TABLE table_name; 




#### ALTER TABLE - ADD Column
    ALTER TABLE table_name
    ADD column_name datatype; 

#### ALTER TABLE - DROP COLUMN
    ALTER TABLE table_name
    DROP COLUMN column_name; 

#### ALTER TABLE - ALTER/MODIFY COLUMN
    ALTER TABLE table_name
    MODIFY COLUMN column_name datatype; 

'''



def connected(func):
    '''
    Coonect to database
    '''
    def wrapper(*arg, **kwarg):
        try:
            connect = mysql.connector.connect(
                host=pswrd.host,
                user=pswrd.user,
                password=pswrd.password,
                database=pswrd.database
            )
            print('*'*star)
            print('Connection to base test_db from MySQL succerfull!')
            print('*'*star)
            func(connect, *arg, **kwarg)
        except Exception as e:
            print('*'*star)
            print(e)
            print('*'*star)
    return wrapper

@connected
def version_db(connect):
    '''
    Test the version
    '''
    with connect:
        cur = connect.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()
        print("Database version: {}".format(version[0]))
        
        print('*'*star)
        
# Прочитать с бази
@connected
def work_with_base(connect, query_text, commit=False):
    '''
    Функция отправляет запрос на SQL сервер,
    query_text - текс запроса
    commit - булевое значение по факту False, когда тру делается комит, который нужен, для записи и 
    обновления  данных
    '''
    
    with connect:
        cur = connect.cursor()
        cur.execute(query_text)
        if commit:
            connect.commit()
            print("Commit done!")
            print('*'*star)
        print("Query done!")
        print('*'*star)
        
def test():
    '''
    lol
    '''
    return None
# -*- coding: utf-8 -*-

import MySQLdb


def connect_bd(host, user, passwd, db):

    try:
        db = MySQLdb.connect(host, user, passwd, db, charset='utf8')
    
    except MySQLdb.Error as err:
        print("Connection error: {}".format(err))
        
    return db

def prnt_tables(db):
    
    cur = db.cursor()
    cur.execute('''show tables''')
    data = cur.fetchall()
    print('All tables from database:\n')
    [print(i[0]) for i in data]
    print('\n')
    
def prnt_one_table(db, name_tabl, max_str = 10):
    
    cur = db.cursor()
    cur.execute('''SELECT * FROM %(name_tabl)s LIMIT %(lim)s'''%{'name_tabl': name_tabl,'lim':max_str})
    data = cur.fetchall()
    print('\nTable name: '+name_tabl+'\n')
    [print(i) for i in data]
        
def one_table(db, name_tabl, max_str = 10000):
    
    cur = db.cursor()
    cur.execute('''SELECT * FROM %(name_tabl)s LIMIT %(lim)s'''%{'name_tabl': name_tabl,'lim':max_str})
    data = cur.fetchall()
        
    return data
        
def one_table_mod (db, name_tabl, start_line = 1, val_line = 10000):
    
    cur = db.cursor()
    cur.execute('''SELECT * FROM %(name_tabl)s LIMIT %(lim1)s, %(lim2)s'''%{'name_tabl': name_tabl,'lim1': start_line, 'lim2': val_line})
    data = cur.fetchall()
       
    return data



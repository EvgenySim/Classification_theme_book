# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.externals import joblib
import time
import bd_work as bd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
    
def predict_model(X_test):
    
    vectorizer = joblib.load('vectorizer.pkl') # загружает модель
    model = joblib.load('model_rfc.pkl') # загружает модель
    
    X_test_vec = vectorizer.transform(X_test).toarray()
    result = model.predict(X_test_vec)
    
    return result
                
def create_test_sample(host = 'localhost', user = 'root', passwd = 'pas', db = 'libgen', start = 0):
    
    db = bd.connect_bd(host, user, passwd, db)
    
    data = bd.one_table_mod(db, 'updated', start)
    meet_frequency = 0.8
    val_data = []
#    for i in data: print(i+'\n')
    
    for i in range(len(data)):
        if data[i][12] == 'English':
            if data[i][13] != '0' and data[i][13] != '':
                try:
                    if int(data[i][13]) >= 250 and int(data[i][13]) <= 261: # править тут 
                        val_data.append([data[i][1], data[i][37]])
                except: pass
                
    data_test = []
    for i in range(len(data)):
        if data[i][12] == 'English':
            if data[i][13] == '0' or data[i][13] == '':
    
                try:
                    
                    f = open(r'D:\\'[:-1]+r'vocs\one\\'[:-1]+data[i][37]+'.txt', 'r')
                    text = f.read().split('\n')
                    
                    new_text = ''
                    max_frequency = 0
                    mas_text = []
                    
                    for j in range(0, len(text)-1):
                        sl = text[j].split(':')
                        if int(sl[1])>max_frequency: max_frequency = int(sl[1])
                        mas_text.append([sl[0], sl[1]])

                    for j in range(0, len(text)-1):
                        if int(mas_text[j][1])/max_frequency>meet_frequency:
                            new_text += ' '+mas_text[j][0]
                    
                    data_test.append([data[i][1], new_text, data[i][37]])
                
                    f.close()
            
                except IOError:
            
                    pass
                
    return data_test, val_data

def record_bd(tabl_bd):
    
    val_error = 0
    db = bd.connect_bd(host = 'localhost', user = 'root', passwd = 'pas', db = 'libgen')
    cur = db.cursor()
    cur.execute('''DROP TABLE IF EXISTS technique_electronics''') # править тут
    cur.execute('''CREATE TABLE technique_electronics (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, title VARCHAR(550), MD5 VARCHAR(550))''') # править тут
    for i in tabl_bd:
        try:
            name_book = i[0]
            cur.execute('''INSERT INTO technique_electronics (id, title, MD5) VALUES (NULL, '%(1)s','%(2)s')'''%{'1':name_book, '2':i[1]}) # править тут
            db.commit()
        except:
            val_error +=1
    
    print(val_error, ' файл(ов) не записалось в базу данных')
        
def main():
    
    t = time.time()
    kol1, kol2, kol3 = 0, 0, 0 
    tabl = []
    
    while kol3 < 1700000: #1700000
        
        data_test, val = create_test_sample(start = kol3)
        X_test = []

        if len(data_test) > 0: 
            
            for elm in data_test:
                X_test.append(elm[1])
    
            res = predict_model(X_test)
            
            for i in range(len(res)):
                if res[i] == 1:
#                    print(i,' - ', data_test[i][0],' - ', res2[i])
                    tabl.append([data_test[i][0], data_test[i][2]])
                    kol1 += 1
                kol2 += 1
        kol3 += 10000
        for i in val:
            tabl.append([i[0], i[1]])
        print(kol1, ' - ', kol2, ' - ', kol3)
    
    record_bd(tabl)
    print('Время выполнения, с :','%.2f'%(time.time() - t)+'\n')
    
    
main()
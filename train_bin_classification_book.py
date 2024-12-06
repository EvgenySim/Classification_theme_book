# -*- coding: utf-8 -*-

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.externals import joblib
import time
import bd_work as bd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def create_model(X_train, Y_train, save_vector = True, save_model = True, val_tree = 30):
    
    vectorizer = TfidfVectorizer(stop_words='english') # можно использовать TfidfVectorizer, но там непонятно с TF-IDF
    vectorizer.fit(X_train) # обучения модели векторов
    if save_vector == True:
        joblib.dump(vectorizer, 'vectorizer.pkl') # выгружает модель
    
    X_train_vec = vectorizer.transform(X_train).toarray() # преобразование строк в вектора
    model = RandomForestClassifier(n_estimators=val_tree, n_jobs=-1) # создание модели RFC из n_estimators деревьев
    model.fit(X_train_vec, Y_train) # обучение модели RFC
    if save_model == True:
        joblib.dump(model, 'model_rfc.pkl') # выгружает модель
    
def predict_model(X_test):
    
    vectorizer = joblib.load('vectorizer.pkl') # загружает модель
    model = joblib.load('model_rfc.pkl') # загружает модель
    
    X_test_vec = vectorizer.transform(X_test).toarray()
    result = model.predict(X_test_vec)
    
    return result
                
def create_train_sample(host = 'localhost', user = 'root', passwd = 'pas', db = 'libgen'):
    
    db = bd.connect_bd(host, user, passwd, db)
    val_train = 30000 # количество примеров для обучения выборки / 500000
    data = bd.one_table(db, 'updated', val_train)
    # бизнес 1-22, экономика 609-620

    data_train = []
    meet_frequency = 0.8 # частота встречи слова в выборке
    for i in range(len(data)):
        if data[i][12] == 'English':
            if data[i][13] != '0' and data[i][13] != '':
    
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
#                    print(mas_text, max_frequency)
                    for j in range(0, len(text)-1):
                        if int(mas_text[j][1])/max_frequency>meet_frequency:
                            new_text += ' '+mas_text[j][0]
                    
#                    print('nn = ', new_text)
                    
                    if int(data[i][13]) >= 219 and int(data[i][13]) <= 222: value = 1 # править тут
                    else: value = 0
                    data_train.append([data[i][1], value, new_text])
                
                    f.close()
                
                except IOError:
                    pass
            
    return data_train

def main():
    
    t = time.time()
    data_train = create_train_sample()
    sum1 = 0
    for elm in data_train:
#       print(elm[0], elm[1], elm[2])
        if elm[1] == 1: sum1 +=1
    print('Считалось файлов с темой: ', sum1)
    X, Y = [], []
    for elm in data_train:
        X.append(elm[2])
        Y.append(elm[1])
#        if elm[1] == 1:
#            print(elm[0])
    print('Считалось всего файлов подходящих для обучения: ',len(data_train)) 
    X_train, X_test, Y_train,  Y_test = train_test_split(X, Y, train_size = 0.8) # все слова обучающей выборки подавать в виде строк
    create_model(X_train, Y_train, val_tree = 50)
    res = predict_model(X_test)
    
    print('Точность: ', accuracy_score(res, Y_test))
    print('Процент файлов с треб. темой от общего числа подходящих, %', sum1*100/len(data_train))
    print('Время выполнения, с :','%.2f'%(time.time() - t)+'\n')    

main() 
from sklearn.datasets import load_iris
from sklearn.neural_network import MLPClassifier
import pymysql
import json
connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True) 
con=connection.cursor()


def get_pulse_prediction(height,weight,age,average_pulse,somato_type):
    con.execute("SELECT id FROM data_pulse_people WHERE id=(SELECT max(id) FROM data_pulse_people)")
    max_id=con.fetchall()
    for i in max_id:
        new_max_id=i[0]
    iris2=[]
    con.execute("SELECT * FROM data_pulse_people")
    iris=con.fetchall()
    for i in range(0,new_max_id):
        iris2.append(iris[i])
    ##print(iris2)

    X=[]
    y=[]
    t=[]

    for j in iris2:
    ##    print(j)
        for i in range(0,7):
            if i!=3 :
                if i!=0:
                    t.append(j[i])
            else:
                y.append(j[i])
        X.append(t)
        t=[]

##    print(X) 
##    print(y)

       
    clf = MLPClassifier(solver='lbfgs',alpha=1e-5,hidden_layer_sizes=(1), random_state=1)
    clf.fit(X, y)
    get_prediction_proba=clf.predict_proba([[height, weight, age, average_pulse,somato_type]])
    get_prediction=clf.predict([[height, weight, age, average_pulse,somato_type]])
    return get_prediction,get_prediction_proba

##print(get_pulse_prediction( 1.2, 12.0, 12,56.0,2))

   

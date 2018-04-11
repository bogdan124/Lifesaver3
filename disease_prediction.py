##from sklearn.datasets import load_iris
##from sklearn.neural_network import MLPClassifier
##iris=load_iris()
##
##X=[]
##y=[]
##for i in range(0,150):
##    if i<50:
##        X.append(iris.data[i])
##        y.append('setosa')
##    elif i>=50 and i<=100:
##        X.append(iris.data[i])
##        y.append('versicolor')
##    elif i>100 and i<=150:
##        X.append(iris.data[i])
##        y.append('virginica')
##
####print(y)          
##    
##clf = MLPClassifier(solver='lbfgs',hidden_layer_sizes=(12))
##clf.fit(X, y)
##while True :
##    input1=input("get the sizes of the sepal  lenght:")
##    input2=input("get the sizes of the sepal width:")
##    input3=input("get the sizes of the petal lenght:")
##    input4=input("get the sizes of the petal width:")
##    print(clf.predict_proba([[input1,input2,input3,input4]]))
##    print(clf.predict([[input1,input2,input3,input4]]))
##
##  














from sklearn.datasets import load_iris
from sklearn.neural_network import MLPClassifier,MLPRegressor
import pymysql
import json
import os






def disease_prediction(maximum_heart_reate,age,sex,blood_sugure,bloodpresure,cholesterol, **disease):
    with open('static/training/data.json') as json_data:
        d = json.load(json_data)
    ##    print(d)


        X=[]
        y=[]
        
    for i in d:
        X.append([i["maximum heart reate"],i["age"],i["sex"],i["blood sugure"],i["bloodpresure"],i["cholesterol"]])
        y.append([i["disease"]])

    ##67,1,160,289,0,2,108
    ##150,17,1,1,145,60
        
##    input1=input("maximum heart reate:")
##    input2=input("age:")
##    input3=input("sex:")
##    input4=input("blood sugure(1-have,0-no have):")
##    input5=input("bloodpresure(145<normal):")
##    input6=input("cholesterol(60 nomral,200-max):")
##    input7=input("disease:")
    t={  "age": age,"sex": sex,"bloodpresure": bloodpresure,"cholesterol": cholesterol,"blood sugure": blood_sugure,"maximum heart reate": maximum_heart_reate,"disease": disease}
##    with open("data.json","a") as myfile:
##        myfile.write(str(t))
    clf = MLPClassifier(solver='lbfgs',alpha=1e-5,hidden_layer_sizes=(12), random_state=1)
    clf.fit(X, y)
    get_prediction_proba=clf.predict_proba([[maximum_heart_reate,age,sex,blood_sugure,bloodpresure,cholesterol ]])
    get_prediction=clf.predict([[maximum_heart_reate,age,sex,blood_sugure,bloodpresure,cholesterol]])
   
    return get_prediction[0]##,get_prediction_proba

print(disease_prediction(67,1,160,289,2,108))

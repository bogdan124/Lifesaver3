import serial
import re
import pymysql

user_id=27
connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True)
con=connection.cursor()


ser = serial.Serial("COM9", 115200)
while True:
        print ser.readline()
        number1=ser.readline() 
##        number=number1[33:]
        if number1>0:           
            sql2="SELECT uname FROM register WHERE id="+str(user_id)+""
            con.execute(sql2)
            fecth=con.fetchall()
            for i in fecth:                
                fecth=i[0]  
            sql1="SHOW TABLES LIKE '"+str(str(fecth)+str(user_id))+"'"
            var=con.execute(sql1)
            if var==0:
                sql="CREATE TABLE "+str(fecth)+str(user_id)+"(id int(15) AUTO_INCREMENT PRIMARY KEY,id_user int,data int(15),time date )"
                con.execute(sql)
            else:
                sql3="INSERT INTO "+str(fecth)+str(user_id)+" VALUES('','"+str(user_id)+"','"+str(number1)+"','')"
                con.execute(sql3)
                   



##trebuie sa selectez data ziua



        
##https://www.livescience.com/53815-what-heart-rate-numbers-mean.html
        

from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify
import pyttsx
import pymysql
import numpy
from gtts import gTTS
from flask_socketio import SocketIO ,send,emit
import os
import os.path
import werkzeug
import time
import sys
import json
from flask import g
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import pygal
from pygal.style import DefaultStyle
from googletrans import Translator
import random
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from pulse_data_learn import get_pulse_prediction
from disease_prediction import disease_prediction
from sklearn.datasets import load_iris
from sklearn.neural_network import MLPClassifier,MLPRegressor
from chat_bot_answear import response_chat_bot
from wikipedia_get_data_bot import show_search_data,show_text_data


##print(get_pulse_prediction( 1.82, 70.0, 120.0, 17,78.0,2))
##my librarys

##from google_data import json_google_data




#http://www.instructables.com/id/Interface-Arduino-to-MySQL-using-Python/#step1
app=Flask(__name__)
##https://bootsnipp.com/snippets/yPDxG
##http://www.webslesson.info/2017/03/load-content-while-scrolling-with-jquery-ajax-php.html
app.config['UPLOAD_FOLDER'] = 'static/profile_pic/'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif','obj','mtl'])
app.config['SECRET_KEY'] = 'mysecret'
socketio=SocketIO(app)
connection=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True) 
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
app.config['GOOGLEMAPS_KEY'] = "8JZ7i18MjFuM35dJHq70n3Hx4"
GoogleMaps(app,key="AIzaSyBAY3X8atcP98Q3qgfuXC6OggI8e1UntQ0")
##GoogleMaps(app, key="AIzaSyBAY3X8atcP98Q3qgfuXC6OggI8e1UntQ0")
con=connection.cursor()

##@app.before_request
##def connecting_mysql():
##    con=connection.cursor()
##
##@app.teardown_request
##def mysql_disconnect(exception=None):
##    con.close()

@app.route("/register",methods=["GET","POST"])     
def register():
    error=None  
    if request.method=="POST":
          user=request.form["user"]
          email=request.form["email"]
          cemail=request.form["cemail"]
          code=request.form["code"]
          pass1=request.form["pass1"]
          pass2=request.form["pass2"]
          if len(pass1)>0 and len(pass2)>0 :
                if pass1==pass2:
                    if code>=0:
                        if cemail==email and len(email)>0 and len(cemail)>0:                      
                              if len(user)>0:
                                    sql="SELECT * FROM register WHERE uname='"+user+"'"
                                    con.execute(sql)
                                    row = con.fetchone()                                                    
                                   
                                          
                                    if row == None:
                                         sql4="INSERT INTO register VALUES('','"+user+"','"+pass1+"','"+code+"','"+email+"','"+"profile_pic/default_profile_pic.jpg"+"','','','','','0','0')"
                                         con.execute(sql4)
                                         return redirect(url_for('login'))       #,id=row[0]
                                    else:
                                       error="we have one in the db"   
                              else:
                                error = "user<0"
                        else:
                         error="emails are not equels and have little characters"
                    else:
                          code=0
                else:
                  error="pass are not equel"
          else:            
            error = "pass<0"
          
    if error != None:     
          return render_template("logout.html",error=error)          
    else:
          return render_template("register.html")



@app.route('/login',methods=['POST','GET'])
def login():
        sql="SELECT * FROM register"
        con.execute(sql)
        error=None
        global uname_general_user
        if request.method=='POST' :
            for i in con.fetchall():
                if request.form['uname']==i[1] and request.form['pass']==i[2]:
                       uname_user=request.form['uname']
                       uname_pass=request.form['pass']
                       sqkl="SELECT * FROM register WHERE uname='"+str(uname_user)+"' AND pass='"+str(uname_pass)+"'"
                       con.execute(sqkl)
                       rewq=con.fetchall()
                       session['connect']='connect'
                       connect=session['connect']
                       session['id']=i[0]
                       id12=session['id']
                       session.permanent=True
                       for i in rewq:
                           admin=i[8]
                           session['medic']=i[7]
                           medic=session['medic']
                           if admin==1:
                               return redirect(url_for("admin",id=session['id'],connect=connect,page='comments'))
                           else:
                                   
                               if str(i[7])=='1':
                                  print(i[7])
                                  id12=session['id']
                                  uname_general_user=uname_user
                                  return redirect(url_for('index',id=id12,connect=connect,medic='1'))
                               else:
                                  return redirect(url_for('index',id=id12,connect=connect,medic=medic))  
                else:
                       error="wrong name or password"
                       
        return render_template("login.html",error=error)



@app.route('/admin',methods=["POST","GET"])
def admin():
     maps=False
     id=request.args['id']
     id13=session['id']
     connect=session['connect']
     page=request.args['page']
     if id13=="":
         return redirect(url_for('logout'))
##     if url=="":
##         return redirect(url_for('logout'))
     if id13==None :
         return redirect(url_for('logout'))
     if id==id13:
         return redirect(url_for('logout'))
     if request.args['connect'] != 'connect':
         return redirect(url_for('login'))
     if request.args['connect'] == '':
         return redirect(url_for('login'))
     if request.args['connect']=="" and request.args['id']=="" and session['connect']=="connect" and session['id']:  
        redirect(url_for('index',id=id13,connect=connect))
     sql="SELECT * FROM register WHERE id="+str(session['id'])+""
     con.execute(sql)
     fetching=con.fetchall()
     if page=='comments':
         select_page_info="SELECT * FROM comments ,comment_2 "
         con.execute(select_page_info)
##     elif page=='reports':
##         select_page_info="SELECT * FROM comments"
##         con.execute(select_page_info)
##     elif page=='profiles':
##         select_page_info="SELECT * FROM register"
##         con.execute(select_page_info)
##     elif page=='medics':
##         select_page_info="SELECT * FROM register WHERE medic=1"
##         con.execute(select_page_info)
##     elif page=='admins':
##         select_page_info="SELECT * FROM register WHERE admin=1"
##         con.execute(select_page_info)
##     elif page=='maps':
##         select_page_info="SELECT * FROM gps_data_user "
##         maps=True
##         con.execute(select_page_info)
     info_page=con.fetchall()
##     supra = pygal.maps.world.SupranationalWorld()
##     supra.add('Asia', [('asia', 1)])
##     supra.add('Europe', [('europe', 1)])
##     supra.add('Africa', [('africa', 1)])
##     supra.add('North america', [('north_america', 1)])
##     supra.add('South america', [('south_america', 1)])
##     supra.add('Oceania', [('oceania', 1)])
##     supra.add('Antartica', [('antartica', 1)])
##     supra.render()
##     supra = supra.render_data_uri()
     return render_template("email.html",fetching=fetching,info_page=info_page,maps=maps)##,supra=supra)

@app.route('/admin_info_content',methods=['POST','GET'])
def admin_info_content():
     maps=False
##     id=request.args['id']
##     id13=session['id']
##     connect=session['connect']
     page=request.args['page']
     if page=='comments':
         select_page_info="SELECT * FROM comments ,comment_2 "
         con.execute(select_page_info)
     elif page=='reports':
         select_page_info="SELECT * FROM comments"
         con.execute(select_page_info)
     elif page=='profiles':
         select_page_info="SELECT * FROM register"
         con.execute(select_page_info)
     elif page=='medics':
         select_page_info="SELECT * FROM register WHERE medic=1"
         con.execute(select_page_info)
     elif page=='admins':
         select_page_info="SELECT * FROM register WHERE admin=1"
         con.execute(select_page_info)
     elif page=='maps':
         select_page_info="SELECT * FROM gps_data_user "
         maps=True
         con.execute(select_page_info)
     elif page=='a_i':
         select_page_info="SELECT * FROM ai_files "
         maps=True
         con.execute(select_page_info)    
     info_page=con.fetchall()
##     supra = pygal.maps.world.SupranationalWorld()
##     supra.add('Asia', [('asia', 1)])
##     supra.add('Europe', [('europe', 1)])
##     supra.add('Africa', [('africa', 1)])
##     supra.add('North america', [('north_america', 1)])
##     supra.add('South america', [('south_america', 1)])
##     supra.add('Oceania', [('oceania', 1)])
##     supra.add('Antartica', [('antartica', 1)])
##     supra.render()
##     supra = supra.render_data_uri()
     return render_template("site_back_info.html",info_page=info_page,maps=maps)##,supra=supra)
 
@app.route('/show_admin_map',methods=['POST','GET'])
def show_admin_map():
##     supra = pygal.maps.world.SupranationalWorld()
##     supra.add('Asia', [('asia', 1)])
##     supra.add('Europe', [('europe', 1)])
##     supra.add('Africa', [('africa', 1)])
##     supra.add('North america', [('north_america', 1)])
##     supra.add('South america', [('south_america', 1)])
##     supra.add('Oceania', [('oceania', 1)])
##     supra.add('Antartica', [('antartica', 1)])
##     supra.render()
##     supra = supra.render_data_uri()
     return render_template("show_admin_map.html"),##supra=supra)
    

@app.route('/',methods=["POST","GET"])
def index():
     id=request.args['id']
     medic=request.args['medic']
     medic13=session['medic']
     id13=session['id']
     connect=session['connect']
     
     if id13=="":
         return redirect(url_for('logout'))
##     if url=="":
##         return redirect(url_for('logout'))
     if id13==None :
         return redirect(url_for('logout'))
     if id==id13:
         return redirect(url_for('logout'))
     if request.args['connect'] != 'connect':
         return redirect(url_for('login'))
     if request.args['connect'] == '':
         return redirect(url_for('login'))
     if request.args['connect']=="" and request.args['id']=="" and session['connect']=="connect" and session['id']:  
        redirect(url_for('index',id=id13,connect=connect))
     if  request.args['medic']:   
        if request.args['medic']=="" or medic!=medic13:
            redirect(url_for('logout'))
     connection_index=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True)
     try:
         with connection_index.cursor() as con:
             sql="SELECT * FROM comments,abonari,register WHERE comments.post_id=abonari.id_user AND register.id=abonari.id_abonat ORDER BY comments.id DESC LIMIT 12 "
             con.execute(sql)
             row=con.fetchall()
             connection_index.commit()
         with connection_index.cursor() as con:     
             sqll="SELECT * FROM abonari WHERE id_user="+str(session['id'])+""
             con.execute(sqll)
             rew=con.fetchall()
             dates="0"
             for z in rew:
                 sqe="SELECT * FROM comments,register,comment_2 WHERE comments.post_id="+str(z[2])+" AND register.id="+str(z[2])+" AND comments.comment_highrehy=1"
                 con.execute(sqe)
                 dates=con.fetchall()
                 connection_index.commit()
         with connection_index.cursor() as con:
                 sqe2="SELECT comment_2.comment,comment_2.comment_id,comment_2.name,register.profile_pic ,register.id ,comments.post_id FROM `comment_2`,comments,register WHERE comment_2.comment_id=comments.id AND comments.post_id=register.id ORDER BY comment_id DESC"
                 con.execute(sqe2)
                 sqe2=con.fetchall()
                 connection_index.commit()
##         with connection_index.cursor() as con:
##                 sql="SELECT * FROM notification WHERE user_towards='"+str(session['id'])+"' "
##                 con.execute(sql)
##                 select_notifi=con.fetchall()
##                 connection_index.commit()
         with connection_index.cursor() as con:
                 sql="SELECT * FROM post_points_notifi WHERE id_user='"+str(session['id'])+"' ORDER BY id DESC "
                 con.execute(sql)
                 select_notifi2=con.fetchall()
                 connection_index.commit()
##         with connection_index.cursor() as con:
##                 sql="SELECT * FROM post_points_notifi WHERE id_user='"+str(session['id'])+"' ORDER BY id DESC "
##                 find_out=con.execute(sql)
##                 if find_out%5==0:
##                     sql="SELECT * FROM tests WHERE id_user="+str(session['id'])+" ORDER BY id DESC"
##                     con.execute(sql)
##                     tests=con.fetchall()                    
##                 else:
##                     tests=0
         with connection_index.cursor() as con:
                 sql="SELECT profile_pic,uname FROM register WHERE id='"+str(session['id'])+"'"
                 con.execute(sql)
                 profile_pic=con.fetchall()
                 connection_index.commit()
         with connection_index.cursor() as con:                 
                 sql="SELECT * from post_points_notifi,questions_post WHERE questions_post.post_id_were_ques_is=post_points_notifi.id_post AND post_points_notifi.id_user="+str(session['id'])+" ORDER by post_points_notifi.id DESC LIMIT 10"         
                 con.execute(sql)
                 find_question_to_show=con.fetchall()
     finally:
         connection_index.close()
     if len(str(dates))==0:
        return render_template("profile.html",row=row,dates=dates,sqe2=sqe2,profile_pic=profile_pic,select_notifi2=select_notifi2)##,tests=tests##select_notifi=select_notifi
     else:    
        return render_template("profile.html",row=row,dates=dates,sqe2=sqe2,profile_pic=profile_pic,select_notifi2=select_notifi2)##,tests=tests)##,select_notifi=select_notifi
      

     
##
##@socketio.on('message')
##def handleMessage(msg):
##	print('Message: ' + msg)
##	sql="INSERT INTO comments VALUES('','22','asd','"+msg+"','1') "
##	con.execute(sql)
##	send(msg, broadcast=True)
@app.route('/select_index',methods=["POST","GET"])
def select_index():
    id13=session['id']
    limit=request.args['limit']
    print(limit)
    start=request.args['start']
    print(start)
##    select="SELECT * FROM comments WHERE post_id="+str(31)+" ORDER BY id DESC LIMIT "+str(start)+","+str(limit)+""    
##    select="SELECT comments.post,comments.name,comments.post_id , register.id,register.profile_pic,comments.id,abonari.id_user,abonari.id_abonat ,( SELECT profile_pic FROM register WHERE abonari.id_abonat=register.id ) FROM comments,register,abonari WHERE abonari.id_abonat=comments.post_id AND register.id=abonari.id_user ORDER BY comments.id DESC LIMIT "+str(start)+","+str(limit)+" "
    connection_index=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True)
    try:
         with connection_index.cursor() as con:
            select="SELECT comments.post,comments.name,comments.post_id , register.id,register.profile_pic,comments.id,abonari.id_user,abonari.id_abonat ,( SELECT profile_pic FROM register WHERE abonari.id_abonat=register.id ),comments.mp3_path,comments.points FROM comments,register,abonari WHERE abonari.id_abonat=comments.post_id AND register.id=abonari.id_user GROUP BY comments.post ORDER BY comments.id DESC LIMIT "+str(start)+","+str(limit)+""
            con.execute(select)
            fetch=con.fetchall()
            connection_index.commit()        
    finally:
         connection_index.close()
##    sql=sql3="SELECT comment_2.comment,comment_2.comment_id,comment_2.name,register.profile_pic ,register.id ,comments.post_id FROM `comment_2`,comments,register WHERE comment_2.comment_id=comments.id AND comments.post_id=register.id ORDER BY comment_id "
##    print(fetch)
    json_fetch=str(jsonify(fetch))
    print(len(json_fetch))       
    return jsonify(fetch)




@app.route('/profile',methods=["POST","GET"])
def profile():
     id=request.args['id']
     id13=session['id']
     global id_general_user
     id_general_user=session['id']
     connect=session['connect']
     if id13=="":
         return redirect(url_for('logout'))
##     if url=="":
##         return redirect(url_for('logout'))
     if id13==None :
         return redirect(url_for('logout'))
     if id==id13:
         return redirect(url_for('logout'))
     if request.args['connect'] != 'connect':
         return redirect(url_for('login'))
     if request.args['connect'] == '':
         return redirect(url_for('login'))
     if request.args['connect']=="" and request.args['id']=="" and session['connect']=="connect" and session['id']:  
        redirect(url_for('index',id=id13,connect=connect))
     sql="SELECT * FROM register WHERE id='"+str(id13)+"'"
     con.execute(sql)
     row=con.fetchall()
     sql2="SELECT * FROM comments WHERE post_id='"+str(id)+"' AND comment_highrehy=1 ORDER BY id DESC LIMIT 12 "
     comments_find=con.execute(sql2)
     messages=con.fetchall()
     sql_profile="SELECT * FROM register WHERE id='"+str(id13)+"' "
     con.execute(sql_profile)
     profilepic=con.fetchall()
     global profle_pic44
     global user_uname
     for jk in profilepic:       
       user_uname=jk[2]
       profle_pic44=jk[5]
     if comments_find!=0:
         for i in messages:
             sql3="SELECT comment_2.comment,comment_2.comment_id,comment_2.name,register.profile_pic ,register.id ,comments.post_id FROM `comment_2`,comments,register WHERE comment_2.comment_id=comments.id AND comments.post_id=register.id ORDER BY comment_id "
##             sql3="SELECT * FROM comment_2 WHERE comment_id= "+str(i[0])+" "
             con.execute(sql3)
             row2=con.fetchall()
             if request.method=="POST":
                     post=request.form[''+str(i[0])+'']
                     if request.form['action'] == ''+i[0]+'':
                        sql5="SELECT * FROM register WHERE id="+str(id13)+""
                        con.execute(sql5)
                        row3=con.fetchall()
     new_sql="SELECT * FROM magazin WHERE user_id='"+str(session['id'])+"'"
     con.execute(new_sql)
     carti=con.fetchall()
     new_sql="SELECT * FROM design_colors WHERE user_id='"+str(session['id'])+"'"
     con.execute(new_sql)
     design_colors=con.fetchall()
     new_sql="SELECT * FROM carti WHERE id_user='"+str(session['id'])+"'"
     carti_var=con.execute(new_sql)
     carti_2=con.fetchall()
     if comments_find!=0 or carti_var!=0:
         return render_template("new_profil.html",id_general_user=id_general_user,row=row,messages=messages,row2=row2,profilepic=profilepic,carti_2=carti_2,design_colors=design_colors,carti=carti)
     else:
         return render_template("new_profil.html",id_general_user=id_general_user,row=row,messages=messages,comments_find=comments_find,profilepic=profilepic,carti_2=carti_2,carti=carti,design_colors=design_colors)


##@app.route('/select_profile',methods=["POST","GET"])
##def select_index():
##    limit=request.args['limit']
##    print(limit)
##    start=request.args['start']
##    print(start)
##    select="SELECT comments.post,comments.name,comments.post_id , register.id,register.profile_pic,comments.id FROM comments,register WHERE register.id=comments.post_id ORDER  BY comments.id DESC LIMIT "+str(start)+","+str(limit)+" "
##    con.execute(select)
##    fetch=con.fetchall()
##    print(fetch)
##    json_fetch=str(jsonify(fetch))
##    print(len(json_fetch))       
##    return jsonify(fetch)



        
@socketio.on('my event', namespace='/test')
def test_message(message):
##    reload(sys)
##    //sys.setdefaultencoding('UTF-8')
    emit('my response', {'data': [message['data'],user_uname,profle_pic44]})
##    sle="SELECT uname FROM register WHERE id='"+str(id_general_user)+"'"
##    con.execute(sle)
##    fetc=con.fetchall()
##    var=str(message['data'])
##    get_points=float(len(var))/2
##    language='ro'
##    tts = gTTS(text=var, lang=str(language))
##    new_path_sound="static/mp3_post/"+str(var)+".mp3"
##    tts.save("static/mp3_post/"+str(var)+".mp3")
##    for i in fetc:        
##        print(i[0])
##        sql="INSERT INTO comments VALUES('','"+str(id_general_user)+"','"+str(i[0])+"','"+str(message['data'])+"','1','"+str(language)+"','"+str(new_path_sound)+"','"+str(get_points)+"')"
##        con.execute(sql)

@socketio.on('connect', namespace='/test')
def test_connect():
    print('connect')

##@socketio.on('disconnect', namespace='/test')
##def test_disconnect():
##    print('Client disconnected')    

        
##@socketio.on('second comment', namespace='/comment')
##def test_message(message):
##    emit('my response', {'data': [message['data'],user_uname,profle_pic44]})
##    sle="SELECT uname FROM register WHERE id='"+str(id_general_user)+"'"
##    con.execute(sle)
##    fetc=con.fetchall()
##    for i in fetc:        
##        print(i[0])
##        sql="INSERT INTO comments VALUES('','"+str(id_general_user)+"','"+str(i[0])+"','"+str(message['data'])+"','1')"
##        con.execute(sql)
##        
##@socketio.on('connect', namespace='/comment')
##def test_connect():
##    print('connect')
##
##@socketio.on('disconnect', namespace='/comment')
##def test_disconnect():
##    print('Client disconnected')   
##    




@app.route('/user_profile',methods=['POST','GET'])
def user_profile():
     id=request.args['id']
     id13=session['id']
     global id_general_user
     medic=request.args['medic']
     medic13=session['medic']
     global __medic13__
     __medic13__= medic13
     id_general_user=session['id']
     connect=session['connect']
     if id13=="":
         return redirect(url_for('logout'))
##     if url=="":
##         return redirect(url_for('logout'))
     if id13==None :
         return redirect(url_for('logout'))
     if id==id13:
         return redirect(url_for('logout'))
     if request.args['connect'] != 'connect':
         return redirect(url_for('login'))
     if request.args['connect'] == '':
         return redirect(url_for('login'))
     if request.args['connect']=="" and request.args['id']=="" and session['connect']=="connect" and session['id']:  
        redirect(url_for('index',id=id13,connect=connect))
     if request.args['medic']=="" or medic!=medic13:
        redirect(url_for('logout'))
     connection_user_profile=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True) 
     try:
         with connection_user_profile as con:
         
                  sql="SELECT * FROM register WHERE id='"+str(id13)+"'"
                  con.execute(sql)
                  row=con.fetchall()
                  connection_user_profile.commit()
         with connection_user_profile as con:        
                  sql2="SELECT * FROM comments WHERE post_id='"+str(id)+"' AND comment_highrehy=1 ORDER BY id DESC LIMIT 12 "
                  comments_find=con.execute(sql2)
                  messages=con.fetchall()
                  connection_user_profile.commit()
         with connection_user_profile as con:          
                  sql_profile="SELECT * FROM register WHERE id='"+str(id13)+"' "
                  con.execute(sql_profile)
                  profilepic=con.fetchall()
                  if comments_find!=0:
                         for i in messages:
                             sql3="SELECT * FROM comment_2 WHERE comment_id= "+str(i[0])+" "
                             con.execute(sql3)
                             row2=con.fetchall()
                             if request.method=="POST":
                                     post=request.form[''+i[0]+'']
                                     if request.form['action'] == ''+i[0]+'':
                                        sql5="SELECT * FROM register WHERE id="+str(id13)+""
                                        con.execute(sql5)
                                        row3=con.fetchall()     
                  sql_select_color="SELECT * FROM design_colors WHERE user_id="+str(session['id'])+""
                  select_color1=con.execute(sql_select_color)
                  select_color=con.fetchall()
     finally:
                  connection_user_profile.close()
     if comments_find!=0:
         return render_template("second_profile.html",id_general_user=id_general_user,row=row,messages=messages,row2=row2,profilepic=profilepic,select_color=select_color)
     else:
         return render_template("second_profile.html",id_general_user=id_general_user,row=row,messages=messages,comments_find=comments_find,profilepic=profilepic,select_color=select_color) 
 
    


@app.route('/second_comments2',methods=["POST","GET"])
def second_comments2():
    id=request.args['id']
    second_comment=request.args['second_comment']
    id13=id_general_user
    if request.method=="POST":
        comment=request.form[''+second_comment+'']
        sql2="SELECT * FROM comments WHERE id='"+str(second_comment)+"'"
        con.execute(sql2)
        rew=con.fetchall()
        for kl in rew:
            sql="INSERT INTO  comment_2 VALUES('','"+str(second_comment)+"','"+str(comment)+"','"+str(session['id'])+"','"+str(kl[2])+"')"
            con.execute(sql)
        
    
    return redirect(url_for("user_profile",id=id13,connect='connect'))



@app.route('/edit_post2',methods=['POST','GET'])
def edit_post2():
    id=request.args['id']
    second_comment=request.args['edit_post']
    id13=id_general_user
    if request.method=="POST":
       post3=request.form['description3'] 
       sql4="UPDATE comments SET post='"+post3+"' WHERE id='"+str(second_comment)+"'"
       con.execute(sql4)
       
    return redirect(url_for("user_profile",id=id13,connect='connect'))


@app.route('/delete_post2',methods=["POST",'GET'])
def delete_post2():
    id=request.args['id']
    post=request.args['post']
    id13=id_general_user
    if request.method=="POST":
        sql="DELETE FROM comments WHERE id='"+str(post)+"'"
        con.execute(sql)
        
    
    return redirect(url_for("user_profile",id=id13,connect='connect'))



@app.route('/back_upload2',methods=['POST','GET'])
def back_upload2():
    id=request.args['id']
    id13=session['id']
    i=0
    if 'file' in request.files:
        f = request.files['file']
        file_path2 = os.path.join('back_pic/', werkzeug.secure_filename(f.filename))
        file_path = os.path.join('static/back_pic/', werkzeug.secure_filename(f.filename))
        exten=file_path[-3:]
        for i in ALLOWED_EXTENSIONS:
           if i==exten:
                f.save(file_path)
                i=1
               
                sql="UPDATE register SET back_pic='"+file_path2+"' WHERE id='"+str(id_general_user)+"'"
                con.execute(sql)
                 
             
    return redirect(url_for("user_profile",medic=__medic13__,id=id13,connect='connect'))


@app.route('/upload2', methods=['POST','GET'])
def upload2():
    id=request.args['id']
    id13=session['id']
    i=0
    if 'file' in request.files:
        f = request.files['file']
        file_path2 = os.path.join('profile_pic/', werkzeug.secure_filename(f.filename))
        file_path = os.path.join('static/profile_pic/', werkzeug.secure_filename(f.filename))
        exten=file_path[-3:]
        for i in ALLOWED_EXTENSIONS:
           if i==exten:
                f.save(file_path)
                i=1
               
                sql="UPDATE register SET profile_pic='"+file_path2+"' WHERE id='"+str(id_general_user)+"'"
                con.execute(sql)
                 
             
    return redirect(url_for("user_profile",medic=__medic13__,id=id13,connect='connect'))






@app.route('/posting',methods=['POST'])
def posting():
     id=request.args['id']
     id13=session['id']
     id13=id_general_user
     connect=session['connect']
     sql4="SELECT * FROM register WHERE id="+str(id13)+""
     con.execute(sql4)
     r=con.fetchall()
     for i in r:
            if request.method=="POST":
                post=request.form["description1"]
                if len(post)>5:
                    if request.form['action'] == 'post1':
                        sql5="INSERT INTO comments VALUES('','"+str(id13)+"','"+str(i[1])+"','"+str(post)+"','1','','','')"
                        con.execute(sql5)
     return redirect(url_for('profile',id=id13,connect='connect'))


    
@app.route('/postsubmit',methods=['POST'])
def postsubmit():
    if request.method=="POST":
        post=request.form["description1"]
        sle="SELECT uname FROM register WHERE id='"+str(id_general_user)+"'"
        con.execute(sle)
        fetc=con.fetchall()
        var=str(post)
        get_points=float(len(var))/2
        language='ro'
        new_path_sound=""
##        generate=random.randint(1000000,101000000)
##        tts = gTTS(text=var, lang=str(language))
##        new_path_sound="static/mp3_post/"+str(generate)+".mp3"
##        tts.save("static/mp3_post/"+str(generate)+".mp3")
        for i in fetc:        
            print(i[0])
            sql="INSERT INTO comments VALUES('','"+str(id_general_user)+"','"+str(i[0])+"','"+str(post)+"','1','"+str(language)+"','"+str(new_path_sound)+"','"+str(get_points)+"')"
            con.execute(sql)
        
            
##            sql5="INSERT INTO comments VALUES('','21','','"+str(post)+"','1','','','')"
##            con.execute(sql5)

    
##@app.route('/postsubmit',methods=['POST'])
##def postsubmit():
##     id13=id_general_user
##     connect=session['connect']
##     sql4="SELECT * FROM register WHERE id="+str(id13)+""
##     con.execute(sql4)
##     r=con.fetchall()
##     for i in r:
##            if request.method=="POST":
##                post=request.form["description1"]
##                if len(post)>5:
##                    if request.form['action'] == 'post1':
##                        sql5="INSERT INTO comments VALUES('','"+str(id13)+"','"+str(i[1])+"','"+str(post)+"','1','','','')"
##                        con.execute(sql5)
##     return "your post has been finished"
    
##@socketio.on('my event')                         
##def test_message(message):
##    emit('my response', {'data': 'got it!'})                      

    
@app.errorhandler(500)
@app.errorhandler(400)
def bad_request(e):
    return redirect(url_for('magazin'))

@app.errorhandler(404)
def page_not_found(e):
    return e

@app.route('/site_info',methods=['POST','GET'])
def site_info():
    connection_2=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True) 
    try:
        with connection_2.cursor() as con:
             sql_new_3="SELECT * FROM magazin "
             con.execute(sql_new_3)
             
             products=con.fetchall()
             connection_2.commit()
    finally:
       connection_2.close()
    return render_template('site_info_first_page.html',products=products,j=0)



@app.route('/magazin',methods=["POST","GET"])
def magazin():
    connection_maps=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True) 
    try:
        with connection_maps.cursor() as con:
            var_new="data:image/jpeg;base64,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"
            sql_get_data="SELECT * FROM gps_data_user"
            con.execute(sql_get_data)
            fetch =con.fetchall()
            markers_1=[]
            for i  in fetch:
                data={
                      'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                      'lat': i[1],
                      'lng': i[2],
                      'infobox': "<div class='poze_div'><h5><b><center>"+i[5]+"</center>"+i[4]+"</h5><img src="+i[6]+" width='297px' height='277px'></div>"
                     }
                markers_1.append(data)   


            connection_maps.commit()
    finally:
       connection_maps.close()
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        
        maptype="SATELLITE",
        markers=markers_1
    )
    return render_template('magazin.html', mymap=mymap, sndmap=sndmap)

##@socketio.on('my event', namespace='/test')
##def test_message(message):
##    emit('my response', {'data': message['data']})
##@socketio.on('my broadcast event', namespace='/test')
##def test_message(message):
##    emit('my response', {'data': message['data']}, broadcast=True)
##
##@socketio.on('connect', namespace='/test')
##def test_connect():
##    emit('my response', {'data': 'Connected'})
##
##@socketio.on('disconnect', namespace='/test')
##def test_disconnect():
##    print('Client disconnected')



@app.route('/cart',methods=["POST","GET"])
def cart():
    prod=request.args["prod"]
    return render_template("cart.html", prod=prod)

@app.route('/logout',methods=["POST","GET"])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/upload', methods=['POST'])
def upload():
    id=request.args['id']
    id13=id_general_user
    i=0
    if 'file' in request.files:
        f = request.files['file']
        file_path2 = os.path.join('profile_pic/', werkzeug.secure_filename(f.filename))
        file_path = os.path.join('static/profile_pic/', werkzeug.secure_filename(f.filename))
        exten=file_path[-3:]
        for i in ALLOWED_EXTENSIONS:
           if i==exten:
                f.save(file_path)
                i=1
               
                sql="UPDATE register SET profile_pic='"+file_path2+"' WHERE id='"+str(id_general_user)+"'"
                con.execute(sql)
                 
             
    return redirect(url_for("profile",id=id13,connect='connect'))



@app.route('/back_upload',methods=['POST'])
def back_upload():
    id=request.args['id']
    id13=id_general_user
    i=0
    if 'file' in request.files:
        f = request.files['file']
        file_path2 = os.path.join('back_pic/', werkzeug.secure_filename(f.filename))
        file_path = os.path.join('static/back_pic/', werkzeug.secure_filename(f.filename))
        exten=file_path[-3:]
        for i in ALLOWED_EXTENSIONS:
           if i==exten:
                f.save(file_path)
                i=1
               
                sql="UPDATE register SET back_pic='"+file_path2+"' WHERE id='"+str(id_general_user)+"'"
                con.execute(sql)
                 
             
    return redirect(url_for("profile",id=id13,connect='connect'))




@app.route('/delete_post',methods=["POST"])
def delete_post():
    id=request.args['id']
    post=request.args['post']
    id13=id_general_user
    if request.method=="POST":
        sql="DELETE FROM comments WHERE id='"+str(post)+"'"
        con.execute(sql)
        
    
    return redirect(url_for("profile",id=id13,connect='connect'))



@app.route('/second_comments',methods=["POST","GET"])
def second_comments():
    id=request.args['id']
    second_comment=request.args['second_comment']
    id13=id_general_user
    if request.method=="POST":
        comment=request.form[''+second_comment+'']
        sql2="SELECT * FROM comments WHERE id='"+str(second_comment)+"'"
        con.execute(sql2)
        rew=con.fetchall()
        for kl in rew:
            sql="INSERT INTO  comment_2 VALUES('','"+str(second_comment)+"','"+str(comment)+"','"+str(id13)+"','"+str(kl[2])+"')"
            con.execute(sql)
        
    select="SELECT * FROM register WHERE id="+str(id13)+""
    con.execute(select)
    vb=con.fetchall()
    for v in vb:
        uname=v[0]
        profile=v[1]
    return jsonify(vb=vb)




@app.route('/edit_post',methods=['POST','GET'])
def edit_post():
    id=request.args['id']
    second_comment=request.args['edit_post']
    id13=id_general_user
    if request.method=="POST":
       post3=request.form['description3'] 
       sql4="UPDATE comments SET post='"+post3+"' WHERE id='"+str(second_comment)+"'"
       con.execute(sql4)
       
    return redirect(url_for("profile",id=id13,connect='connect'))


##
##
##@app.route('/load_likes',methods=['POST','GET'])
##def load_likes():
##    com_id=request.args['com_id']
##    sql3="SELECT * FROM likes WHERE com_id="
##


@app.route('/test',methods=['POST','GET'])
def test():
    return render_template("test.html")

@app.route('/_add_numbers')
def add_numbers():
    sql2="SELECT * FROM comments "
    comments_find=con.execute(sql2)
    messages=con.fetchall()
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=messages)



@app.route('/search_index',methods=['POST','GET'])
def search_index():
    if request.method=="POST":
        search=request.form['searching']
        sql_search="SELECT * FROM register WHERE medic=1 AND uname LIKE '%"+str(search)+"%' ORDER BY points DESC LIMIT 20 "
        conn=con.execute(sql_search)
        if conn==0:
            flash("nothing found")
        get=con.fetchall()
##        return redirect(url_for("index",medic=session['medic'],id=session['id'],connect='connect'))
        var = jsonify(get)
        
        return jsonify(result=get)
        




@app.route('/medic_profile',methods=['POST','GET'])
def medic_profile():
     id=request.args['id']
     id13=session['id']
     global id_general_user
     medic=request.args['medic']
     global user_friend_id
     user_friend_id=request.args['medic_id']
     session["user_friend_id"]=user_friend_id
     medic13=session['medic']
     id_general_user=session['id']
     connect=session['connect']
     if id13=="":
         return redirect(url_for('logout'))
##     if url=="":
##         return redirect(url_for('logout'))
     if id13==None :
         return redirect(url_for('logout'))
     if id==id13:
         return redirect(url_for('logout'))
     if request.args['connect'] != 'connect':
         return redirect(url_for('login'))
     if request.args['connect'] == '':
         return redirect(url_for('login'))
     if request.args['connect']=="" and request.args['id']=="" and session['connect']=="connect" and session['id']:  
        redirect(url_for('index',id=id13,connect=connect))
     if request.args['medic']=="" or medic!=medic13:
        redirect(url_for('logout'))
     sql="SELECT * FROM register WHERE id='"+str(user_friend_id)+"'"
     con.execute(sql)
     row=con.fetchall()
     sql2="SELECT * FROM comments WHERE post_id='"+str(user_friend_id)+"' AND comment_highrehy=1 ORDER BY id DESC LIMIT 12 "
     comments_find=con.execute(sql2)
     messages=con.fetchall()
     sql_profile="SELECT * FROM register WHERE id='"+str(user_friend_id)+"' "
     con.execute(sql_profile)
     profilepic=con.fetchall()
     sql_select_liked="SELECT * FROM likes WHERE liked=1 AND user_id="+str(session['id'])+" AND "+str(session['user_friend_id'])+""
     con.execute(sql_select_liked)
     fetch_liked=con.fetchall()
     print(fetch_liked)
     for y in fetch_liked:
         print(y[3])
     if comments_find!=0:
         for i in messages:
             sql3="SELECT comment_2.comment,comment_2.comment_id,comment_2.name,register.profile_pic ,register.id ,comments.post_id,comment_2.id_quest FROM `comment_2`,comments,register WHERE comment_2.comment_id=comments.id AND comments.post_id=register.id ORDER BY comment_id"
             con.execute(sql3)
             row2=con.fetchall()
##             if request.method=="POST":
##                     post=request.form[''+i[0]+'']
##                     if request.form['action'] == ''+i[0]+'':
##                        sql5="SELECT * FROM register WHERE id="+str(id13)+""
##                        con.execute(sql5)
##                        row3=con.fetchall()
         

    
     if comments_find!=0:
         return render_template("user_profile.html",id13=id13,user_friend_id=user_friend_id,row=row,messages=messages,row2=row2,profilepic=profilepic,fetch_liked=fetch_liked)
     else:
         return render_template("user_profile.html",id13=id13,user_friend_id=user_friend_id,row=row,messages=messages,comments_find=comments_find,profilepic=profilepic,fetch_liked=fetch_liked) 


@app.route('/abonare',methods=["POST","GET"])
def abonare():
    id_user=session['id']
    id_abonat=session["user_friend_id"]
    print(id_user)
    print(id_abonat)
    sql_search="SELECT * FROM abonari WHERE (id_user="+str(id_user)+" AND id_abonat="+str(id_abonat)+")"
    how=con.execute(sql_search)
    if how==0:
        sqlo="INSERT INTO abonari VALUES('','"+str(id_user)+"','"+str(id_abonat)+"')  "
        con.execute(sqlo)
#    return redirect(url_for("medic_profile",medic=session['medic'],id=session['id'],connect=session['connect'],medic_id=session['user_friend_id']))

        return "You have been abonated with succes"
    else:
        return "You are abonated already"

@app.route('/new_header_for_profiles',methods=["POST","GET"])
def new_header_for_profiles():

    connection_header=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True)
    try:
        with connection_header.cursor() as con:
                 sql="SELECT * FROM post_points_notifi WHERE id_user='"+str(session['id'])+"' ORDER BY id DESC "
                 con.execute(sql)
                 select_notifi2=con.fetchall()
                 connection_header.commit()
        with connection_header.cursor() as con: 
                 sql="SELECT profile_pic,uname FROM register WHERE id='"+str(session['id'])+"'"
                 con.execute(sql)
                 profile_pic1=con.fetchall()
        with connection_header.cursor() as con:                 
                 sql="SELECT * from post_points_notifi,questions_post WHERE questions_post.post_id_were_ques_is=post_points_notifi.id_post AND post_points_notifi.id_user="+str(session['id'])+" ORDER by post_points_notifi.id DESC LIMIT 10"         
                 con.execute(sql)
                 find_question_to_show=con.fetchall()
        with connection_header.cursor() as con:
                 sql="SELECT * FROM post_points_notifi WHERE id_user='"+str(session['id'])+"' ORDER BY id DESC "
                 find_out=con.execute(sql)
##                 if find_out%2==0:
                 sql="SELECT * FROM tests WHERE id_user="+str(session['id'])+" ORDER BY id DESC"
                 con.execute(sql)
                 tests=con.fetchall()                    
##                 else:
##                     tests=0          
    finally:
         connection_header.close()
    return render_template("new_header_for_profiles.html",profile_pic1=profile_pic1,find_question_to_show=find_question_to_show,tests=tests,select_notifi2=select_notifi2)



@app.route('/likes',methods=["POST","GET"])
def likes():
    com_id=request.args['com_id']
    sle="SELECT * FROM likes WHERE user_id='"+str(session['id'])+"' AND friend_id='"+str(session['id'])+"' AND com_id='"+str(com_id)+"'"
    lee2=con.execute(sle)
    if lee2==0:
       sqlmyqsl="INSERT INTO likes VALUES('','"+str(session['id'])+"','"+str(session['user_friend_id'])+"','"+com_id+"','"+str(1)+"')"
       con.execute(sqlmyqsl)  
    return "liked "


@app.route('/dislikes',methods=['POST','GET'])
def dislikes():
    com_id=request.args['com_id']
    sqlmyqsl="DELETE FROM likes WHERE user_id='"+str(session['id'])+"' AND friend_id='"+str(session['id'])+"' AND com_id='"+str(com_id)+"'"
    con.execute(sqlmyqsl)  
    return "disliked "



@app.route('/like_page',methods=["GET","POST"])
def like_page():
    return render_template("likes.html")



@app.route('/subscription',methods=["GET","POST"])
def subscription():
    select="SELECT id_user,id_abonat FROM abonari WHERE id_user="+str(session['id'])+""
    sel=con.execute(select)
    print(sel)
    get=con.fetchall()
    if sel>0:
        for i in get:
            print(i[1])
            select2="SELECT * FROM register WHERE id="+str(i[1])+""
            con.execute(select2)
            fecth=con.fetchall()
            return render_template("subscription.html",get=get,fecth=fecth)    
    elif sel==0:
        return render_template("subscription.html",get=get)


@app.route('/favorite',methods=["GET","POST"])
def favorite():
    return render_template("favorite.html")



@app.route('/colors_design',methods=["POST","GET"])
def colors_design():
    if request.method=="POST":
        header=request.form['color1'];
        background=request.form['color2'];
        content=request.form['color3'];
        font_size=request.form['color4'];
        font_color=request.form['color5'];
        profile=request.form['color6'];
        sql_select="SELECT * FROM design_colors WHERE user_id="+str(session['id'])+""
        fd=con.execute(sql_select)
        print(fd)
        if fd>0:
          sql="UPDATE design_colors SET header='"+str(header)+"',Background='"+str(background)+"',Content='"+str(content)+"',font_size='"+str(font_size)+"',font_color='"+str(font_color)+"' WHERE user_id='"+str(session['id'])+"'"
          con.execute(sql)
        elif fd==0:  
          sql="INSERT INTO design_colors VALUES('','"+header+"','"+background+"','"+content+"','"+font_size+"','"+font_color+"','"+profile+"','"+str(session['id'])+"') "
          con.execute(sql)


@app.route('/file',methods=["POST","GET"]  )      
def file():
    return render_template("file.html")

##https://www.tutorialspoint.com/flask/flask_file_uploading.htm

@app.route('/magazin_insert',methods=['POST','GET'])
def magazin_insert():
    error="finished"
    if request.method=="POST":
        book_name=request.form['book_name'];
        book_price=request.form['book_price'];
        book_description=request.form['book_description'];
        book_content=request.form['book_content'];
        book_user_id=session['id'];
##        book_file=request.form['book_file'];
        i=0
        file_path2=""
        if 'file' in request.files:
            f = request.files['file']
            print(f)
            file_path2 = os.path.join('magazin_pic/', werkzeug.secure_filename(f.filename))
            file_path = os.path.join('static/magazin_pic/', werkzeug.secure_filename(f.filename))
            exten=file_path[-3:]
            for i in ALLOWED_EXTENSIONS:
               if i==exten:
                    f.save(file_path)
                    i=1

                    error="finished"
               else:      
                    error="error 1:file type "
        sql="INSERT INTO magazin VALUES('','"+str(book_name)+"','"+str(book_price)+"','"+str(book_description)+"','"+str(book_content)+"','"+str(file_path2)+"','"+str(book_user_id)+"')"
        con.execute(sql)         
        return error





@app.route('/bratara',methods=['POST','GET'])
def bratara():
     id=request.args['id']
     id13=session['id']
     connect=session['connect']
     if id13=="":
         return redirect(url_for('logout'))
##     if url=="":
##         return redirect(url_for('logout'))
     if id13==None :
         return redirect(url_for('logout'))
     if id==id13:
         return redirect(url_for('logout'))
     if request.args['connect'] != 'connect':
         return redirect(url_for('login'))
     if request.args['connect'] == '':
         return redirect(url_for('login'))
     if request.args['connect']=="" and request.args['id']=="" and session['connect']=="connect" and session['id']:  
        redirect(url_for('index',id=id13,connect=connect))
     sql="SELECT * FROM register WHERE id="+str(session['id'])+""
     con.execute(sql)
     data_user=con.fetchall()
     for i in data_user:
         uname=i[1]
     select_table="SHOW TABLES LIKE '"+str(uname)+str(session['id'])+"'"
     table_number=con.execute(select_table)
     if table_number==1:
         sql1="SELECT * FROM "+str(str(uname)+str(session['id']))+" WHERE data=(SELECT MAX(data) FROM "+str(str(uname)+str(session['id']))+" ) ORDER BY data"
         con.execute(sql1)
         fecth_data=con.fetchall()
         avg_pulse="SELECT avg(data) FROM "+str(str(uname)+str(session['id']))+""
         con.execute(avg_pulse)
         pulseavg=con.fetchall()
         select="SELECT data FROM "+str(str(uname)+str(session['id']))+" ORDER BY id"
         con.execute(select)
         data=con.fetchall()
         graph = pygal.Line()
         graph.title = 'Your Pulse this week'   
         t=[]
         for i in data:
             t.append(i[0])
         graph.x_labels = map(str,range(2000,2018))
         graph.add('Pulse',t)
    
         graph_data = graph.render_data_uri()
         return render_template('bratara.html',fecth_data=fecth_data,pulseavg=pulseavg,data_user=data_user,graph_data=graph_data,t=t,table_number=table_number)

     else:
         return render_template('bratara.html',data_user=data_user,table_number=table_number)
        

@app.route('/disease_prediction2',methods=['POST','GET'])
def disease_prediction2():
##    if request.method=="POST":
        age=float(request.form["age"])
        sex=float(request.form["sex"])
        bloodpresure=float(request.form["bloodpresure"])
        cholesterol=float(request.form["cholesterol"])
        blood_sugure=float(request.form["blood_sugure"])
        maximum_heart_reate=float(request.form["heart_reate"])
        disease=float(request.form["disease"])
        print(age)
        with open('static/training/data.json') as json_data:
            d = json.load(json_data)
        X=[]
        y=[]      
        for i in d:
            X.append([i["maximum heart reate"],i["age"],i["sex"],i["blood sugure"],i["bloodpresure"],i["cholesterol"]])
            y.append([i["disease"]])
##        t={  "age": age,"sex": sex,"bloodpresure": bloodpresure,"cholesterol": cholesterol,"blood sugure": blood_sugure,"maximum heart reate": maximum_heart_reate,"disease": disease}
##        t = numpy.array(t, dtype=numpy.float64)
        clf = MLPClassifier(solver='lbfgs',alpha=1e-5,hidden_layer_sizes=(12), random_state=1)
        clf.fit(X, y)
        get_prediction_proba=clf.predict_proba([[maximum_heart_reate,age,sex,blood_sugure,bloodpresure,cholesterol ]])
        get_prediction=clf.predict([[maximum_heart_reate,age,sex,blood_sugure,bloodpresure,cholesterol ]])
        save=get_prediction_proba[0][0]
        print(get_prediction_proba)
        for every in range(0,4):
            if get_prediction_proba[0][every]>save:
                save=get_prediction_proba[0][every]
            
                
##        print(get_prediction_proba[0][0])
##        print(get_prediction_proba[0][1])
        
##        print(get_prediction)
        send_this=[save,get_prediction[0]]
        return json.dumps(send_this)
##        disease2=disease_prediction(maximum_heart_reate,age,sex,blood_sugure,bloodpresure,cholesterol)
##        print(disease2)    
##        return jsonify(disease2)












        
##    connection_maps=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True) 
##    try:
##        with connection_maps.cursor() as con:
##            sql_get_data="INSERT INTO "
##            con.execute(sql_get_data)
##            fetch =con.fetchall()
##            connection_maps.commit()
##    finally:
##       connection_maps.close()
##        disease=disease_prediction(heart_reate,age,sex,blood_sugure,bloodpresure,cholesterol)
##    return disease


@app.route('/years_user_number',methods=['POST','GET'])
def years_user_number():
    if request.method=="POST":
         form_element=request.form['years']
         sql_new="UPDATE register SET years='"+str(form_element)+"'  WHERE id='"+str(session['id'])+"'"
         con.execute(sql_new)



@app.route('/years_user_number2',methods=['POST','GET'])
def years_user_number2():
    if request.method=="POST":
         form_element=request.form['years']
         sql_new="UPDATE register SET years='"+str(form_element)+"'  WHERE id='"+str(session['id'])+"'"
         con.execute(sql_new)



@app.route('/abonari_page',methods=["POST","GET"])
def abonari_page():
    return "i have to make the page"




##@app.route('/maps',methods=['POST','GET'])
##def maps():
##
##    return render_template('maps.html', mymap=mymap, sndmap=sndmap)
##    


##def  json_google_data():
##
##    return markers



  
@app.route("/maps",methods=['POST','GET'])
def mapview():
    connection_maps=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True) 
    try:
        with connection_maps.cursor() as con:
            var_new="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMVFRUXGBgVFRcVFhcWFxYWGBcYFxYXGRYYHSghGBolGxcVITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGhAQGy0lHx8tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAMMBAwMBIgACEQEDEQH/xAAcAAACAwEBAQEAAAAAAAAAAAAEBQIDBgABBwj/xAA+EAABAgQEBAMHAgYABgMBAAABAhEAAyExBBJBUQUiYXGBkaEGEzJCsdHwweEHFCNSYvEVQ3KCotIzU4MW/8QAGQEAAwEBAQAAAAAAAAAAAAAAAAECAwQF/8QAIxEAAgICAgICAwEAAAAAAAAAAAECEQMhEjEiQUJRBBMyFP/aAAwDAQACEQMRAD8AD9k05UDtDfFY7KYScKnAIFWgLieNreOGWK5HbySjoccU4+MprHzDjnFVLUawVxniGjxm1qcxtiwRgYTytluGlFamjb8JQJSQYxmCm5S8HYnjFGEXONihk4jrjntMojKI8/h7wwYifMmzBmTKSFEH+9R5S2rMo+UY6ZMJLmPoP8M5rSMSAA+eXXViFU629YcMaj0TKbk7NohydGpqH7OWgxJIBSci0KBC0KGZBGoUkuPSE2EnEqNHLd26/tD2W5SMhCNyZSSDuHcN4iNeCaM+bTMB7a+wWRBxOCBMsB5shyVSxfOguSqW1xUjch8vziP0NKUuUtKwoM+XlysH0LAP9do+efxF9kEJH87hQBJWoCdLH/JmKN0gWlk0b5TSxDZJ1pmjV7QD/DvhWdecjtH3rhOGASA0fMP4dKloSBrH1XCYpDCseZllym2zuguMUgr+WETlyQI44tLXhVjuLJBZ4WkGx9LIjyaYW8OnZg8GTFRp6IrZFUQVHZolEMoqiQEetAnEOIJlBrqNht1PSBJvSC6Lp6wkOS35pvCqfxdIdg7fmgMATJi5inUafjU0ERmyWDeNr9o64fjKrkc8s2/EYYDiRWWUB4P5l/0hkFRksMv+ok6Ox1vQxqAYieJQei4zclssUuKVmOKogTAB48cTESYiowAeKMVKMTJipcICBMdESY6FYHyyRMYM8ezcGVCE+A4kFKrGvwM9BGkaPJI0jhgYrG8CJMCf/wA6esfQ5wT0gaYtAiFmn9lPDAwUzgShFcvgSzG3XiUbCPZU9HSKeaaEsEDJy/ZvcRrfY/hvukTQNSg30GYfrF/vkdIM4ZihnyhhmGXubj1EGPLLmrDJhjwdE0lKFjMHGl/xo0PD+ISlEIzhL00ANLOGD9IQ8UkZklhzDSAOGKUSULWpD1ScrAeQZj3BeO9PZ58o6NZicNkU1QLpKM79a1YWpYN4QOOIoClIWoqTMdK0TB8SSGIdIYhtfWkQ99OQHU5H93Kq3UsoN1Gl6wk4viMoJCiXZhzBlaHqKC/lrE5IlY5F0zgYkLeUomWrmlq3TseosYZyMatIhV7Mca98FYeYCkAlibpWDq+hdoLxqVIDhYOhFQQRe+0eVkxSb0enjyQryGZ4nMIgNJUV5lVECSJ6iQ5ABatxXWDfdGpKqC+g6+MR+nJ9F/sxfZrOC44EMIdAvGR4fj5coWJa5H5eHMr2kw9nPiDFxhNLaOebjehsExZkgFXGsOkOZifOEuO9uJL5ZPORVSvlQNyeu0PixWN+M8RTIQ/zF8o/U9IyiJhmHMSST1r0JG8IMfxleIml+arCoone9tW8I0mBQ6Qlgf8Au16hIbweOvDjS2c+STYdJlAtQlquwbwIvHnEJQyGjef6/UdbwZmyJqCHq9T5APAfEFgooxJ6u4cPQh6U87x0NmaiKcAg+/lhzVQ+sayYYScEwZ94Hsly/oIdzY5cj2bxKyYgTHpMRMQMiTESY9MQJhAeGIKiRiCoBFZjo9MdCA/OMslJpGl4bjlMKwkXLEPOFgMI1ytNGmNcWFqxyjuYHnTJh0g1KA8XmTSObkkdHGxIAt4KlSFdYJMit4LloA3glIIoHlYVUWe5UCCCx0Ox0PnB8lQ0AijEg9IFMcoWjS4maJyBNRQn4kj5Vahu9ukC4LiAT85SxDjJnALt8J+HumsdwuUoSVT0tmLpOvw9OsKsDhVYidnRmAKXd8tdQ4UnXcx6cJXVHmTjV2av+ZlqY8oLago8isB+1YRcfOZKuaWC2WrKT0C1M7FgOhra+k4dwNKUuACelNLBIf6tFuLwCVDmYijhSbjo29exSOytJdGMez5Jh8X7qYSxQQQCDVgCHH0r0hwOMLxE4kACWVDKklgSyRd9ST6xo+IezEiZUEqAyhkEUS9Ek6sDQ/29gCLhBKly5aZaQFBRBJFFEM43BCS6SHonrHM8duzdZNUTlSzJIWUqqQAmqilTAkFx0J6ViziysqeaYxyGaoOzhLjLlIcly7tA/EcWUJBUSc4dkud2eaSGJetP3hx2cqejMhPMZZM0kBIGVwCmnLy06MNxFoRHh+Ozl3IzEy0g6qFGG1/Foq4jxtIZAfMfBjapGjAV6wBg8GqXMzFsoKQoBxorK52zBIfqPG+XNCyVAhE2gUlqgsoskmig4YDrDqhWBcRx7JJCkvs7qUK2AowOrx7gVn+WQQwK80w/5VZIO/KDTrF3/BpcwsAZawSOdGUF6poLkh6j/I2ECYXhM9DJU+QWaoArcNQGujxlJGkZGm9nMKCaiiWAJa7VVtGwkyCVPY2JzN5B/wBIWeznDyEZVi9QzihFCw1hzJkMXMwFv8AVN2f9NI0j0S2RmSSH/qFPTL9TRz3MUh6AnMXoSALt9olieLoH9NCSSaEsw+3pExLEshZqCHGjnbppESouPWx1w/C5EkuCaCmmv6iITzWLMAFCUCv41OtXdRdvAMPCBcSaxzN27NKpHhMRJirNESuCxFhMRJiBXEfeQCJkxEmIGZEDNhWCJmOir3sdAM+GYiUwgrhTwJNmEpi7hUw2ivibLseopE1zmipKSYK/lQRHLJ0zpUbQMJwfWCEqeyfOKFy2NIITFN2iVHYThwekdiUUvEsIYtnkRmm7NmlQu4fxn3E7IaonBlDZQsobbeMHcGBM7OlIWAXa6gzDMg7ixArbeM1xCSVzeU8wNLMz1JOjRqJcgyJSZctOdfzsxDq3zKodCzioNBb1MKaWzx80k26HeK46TyoJSaAKI1cVbTsAfSF8zic05VTeZIdKspAIKf6g6OGW2hcCtGACeVTghTZlOaA/FqXzNmTR3yg3cQXMckj4pepLhR+DMp90hQA/6jvGxidw2UUpTPzEKGYMCSJtCRe4Lktdlq2LF4ySpOUAEJKWS18qhzLURUMlyP8AJXR4oXiM0tUpIBSAkpTfOQc2lCl8hvZZBAgadjVJkrJUy0qCV5jsXITS5OfdwtV2EFaD2W4HFCdPVKTL92hJJKiAS6ClwBb/AOtfh4QLhFKMzndTIVnl1qqWUEs2hUsUGwvAHGcKvDhM2UVZV85WTR+Vk0swLWqDWG2LxDZVsCmZmCWDK5kLKiCGZRYHoRWM2zRIDTRJyZgM5DlgUsoAkJDsCSlwa0i/iEnN7ua7zSFKQpKQysvxJyd1pVTZTQLImpMwoU7EpAoHzCcFKU2uYjp8DQ29sJKitGHlJb/45ksAuASkpmBwHACpb3rW2q5D4hZW0xAWCUFAVnAB+EJZIHzVBFP707gA3CYdSGqFkkfKMsugcAalk/S4IgbBFTpkzQCUJIUwqQMqUhOo5koBNXzFrGGuCxCJnItTLLLSSRmWWdy3WZbpS9GIZcM4lLKf6iSC7Fwaq/XfpDadh5a0g5Ur7gHwH3eEMvA8pSRUjKQ/KaAN5Akno0E4WcqWllskMXqwDXv0Y7UhpiaM/wAUy++JSlIIcBWZJGrgJUlzs4JF7Q8BT7qSlVVKmJSlhcOMxba0D+0MiWmUmcGy3fqah3rdqRd7MLE1YmKYkBkahKenU6mMctI2g7RpZ0LZyIZzVCApyxGBoAKTFSkwUuYIHXNEDEVERAiPV4gRQvFCJCj1UVKMVTMWIHXjBvAOgt49hb/OiPYYUfKUI5Yt4UjmjzCB0xdgUkKht9m1dD1MoNBCaCBkrpFwVSOWStnVHopmBzF2SkDTSXpF8s7mLqkR7LJVIhPnbRLsIoUm58BvDjHYTlSI4WVlOeoJqlhUBzV+8PZGGyS8xKnIKiU1yihCsuwL+OhhGFAeI/KaQ94Ni0rSZalFOWoUCdTWwZqAx6MZHlyiVDmBYgBYFXuFUUTTlOjm7il2jj1sfdKBXRzRluAA5CTdkgP00YRypZWQEgAgcpSo0DkO2Usb3IMNTg5KEvPnS0ilJuQpB7nTr16RXKyONCjh0l1gk1zUersfiCm6jmZwxs5MQ9v8CEFBdSUl1UpUsSdHFAcp3O8aDheJwOYITiJClE0yzEHNsAApKnDOwezCI/xA4QZ2FHugFkKcNrlcKFyxuNK9qu6i7CrkgLgWE97w5iQSxYFiKZcg7MgD8BjOz/eGWUv8HvJla5QMmUJapOajdVGNv7Myvd4RCSClgSyvlcknwZ/MbwkxfCiZs3lLkZkmjAlQBQCNWYPu92jGT6Zql2hZwie+JzLCcoC5iUiwMsDMW15kp3uOsa72R4UqZPmT1VUmWE3LFZQkK7MA1NztGP4dw1VVJS5UBlIFs6PdNbQteoygx9U9nMOJUnKNi51dqVG7kxPbG9I+ccEmLxGKmJcstauYUyozjOKbpSkXoWZmeNPxpBQsFKVJClDMcw+WxFOUUDM1LAvVd7BYXLisQ1UJUeZmcklRFOreUaTi+AVMmOUlrJZQZuoo/hGik3HRLilIrwczMcjvRLFqUBpV8rsm9ma5i2dOoUqWPlLkOd1BR+UF2Y6daxdguGHKCE75mYN1DXvd9LRVNUUqANS4NQEktqw8PLwiba7Cr6DpchBQZSwChQYOQKmtgzUfy6QFg8IZKmDMAwIo48IPw0o+7ytV3Bs+r3Or/hiUyU4tUbWhvaEtCzEcYAcPaFs/jY3hTxmT/WWCcpd2MLjJG8edKUk6o9COOLVjqZxvrFC+MPrCyXhxvEJipaXdQhc5P0Vwgg5fFDFCuImEuN4zKRaphPN46TQCNI4ssvRnLJiiatePO8CzuJgXMZWbjZitT4R5KlkhlEuY6I/iy+TMJfkx+KNAeOo/ujozcyQkG58I6Nf88TL/AESLOHHlFYukLAXd4o4YnlEWGXzWjnfbOpPSH0tYbeLUPoIhw6SGh1Jkho5pyOmKEU5G8FYYbCCcYUjaK5Sj2io20J6YVKkbtAXEGBCR6wbLWRcws4gp1UHpFY15EZn4A01VDct3EUYbEKCgpL0NjuGLQSqSSLHxDH9oqwiS6qWNAR50eOo4hpg1LxCwhKClarvUDUktGcx3CCrETcyivIoJJUXIvbo4Ijd+zWPTKnOWCSwJIUyW7P2/Giv2q4UqXPOLkgzJSwBMSkOwcksBarl7OVO1xpirf2RmuqR8tVh0JnlC5SphLJQAvIHUU5TQF/nDdRWldTJ9rZuDmshS1yHZUiav3pSKAhMwgFwLfhjkYnCmYmaJiQoA0UCVp3bfWveFHtbOQFOlKsxAYlwGL8zEXoY2dukjCL3s+x4zFIm4dOIkqdJAU4NgbloV4RTpSvNmYtUlIypBJc75tejQk/h0Ff8AC5gJcKJCBqOavrD3C4Iol5fh1r9DWlD66XGMv6N4/wAhHBsOzPU18VEJB8HzV6C0ajh8tRR7xRASA4LtZ3JO2x2hZgMMooUQa3At2D726VhZ/EfjypPDFSkuJk0KRRhRR571+HMHgj3QpdWLOJ+1y+f/AIfKTkDD38x2VaqEJamxJHZr4vhXEJmIKivik8TykKly5KJiUqW6syFqSEpDBKS7Ec/Qwy9leJJmSshKczAKSq4LM/UUEUcN4dLw06bOmEISHy1DJBqwYuTp0EbRSVo55zkOeC+0nEZGIlSlTRORMCqLSlwpItmAGxh8faCXMnWAV8yWYvq409YRexWGOLxX88se7w8kFMrM7rUQxV1/eNEvh8tU50oZy5Ntaa3/ADRo5sz3o68KteQ/wc4EUAH+IDV7QckPClKMhCXZ/wALgadf3hjh101/OsON1sUu9Ga9seF5yFB0lqkftHzjiOHmJUUlRCu94+y8XlEgFy/dnG2sYj2k4JnSSkB0hyde0UhWYpU1bMJhJ1aBl4datSSbCLStqKcNQhrN+sFYYZw6bW6w7oXYkmcOUNj0jjgVAAAVd4eScKS7bMIg+QhId94rkyeKBZGHsGrv3pBE/C1FdWBEEe7YipMWTJLANX1g5BxFhQRRhSOgtSWozx0HIKE/BpnKIJnTS9qQv4MTlDQZiUnUxySXkzti/FDjAYgtDBC1GF3C0vDzDoAjnlSZ0wtgS5Ri+XJ3MX4jpTwgJR3JMP4h7DEqSBv+bwJlckio66eJpEVzaR3Cl1LjxeNMCfbMPyHqkN/5ZKkgpo9wG+kCJwQCiWdqfhg+VMHwig3I/UaRbKlObeL3+v0jofZyoAnJDMbeFHv3i/AY2cjmlKDGhYApegc6gWsK7s7TmoB0pr0iudJDVNgWsPRz6iEuxjPD4bDYlRGJw6HLOtDFJVepTUWs9xUQr9t/ZfCS5SvcSZYNTmOhvbZn7NBHDpSiHdR5gwAVQVIZRLJF6D0vFfH3VKyAUAchLHMdEhgzVA/K6OTSJUU2Zv2d4mJOHEtNSXfUPmf8/wBRpsPxpRABSCOtKbU6EeUYGaShTMGDB9yBU+Z9I03B1EgF6Dt5+UYuTbs2UUje4HiHJnYhncO71aF/tljMPPky0TMoUSUpUR8KVhzR9wKbpFoHweJzBQJNB61Dtvr4woxGGVOGQgv8aVXvcdwGPnEvI4jWNMZJ/hvglSgorXLKR8SVkC2m0LMN7NYJK3TLVPILCZilrKH0yyhVQftaG61FcpCZgIyNsxAtYnTubw84Nw4EZSz3oCPQUYbaxtCbkYzgosXYPhc2YW966U2ShOVCegSAWFNQ/eNbwvgaEsWruWPkwgzBYIpNmH5u7dhDZDJEXwRDmzM8SwxMwAUYOQ1TpfeOlym/2foYc5QVdfzVoBnyyVEE27/aE1oEwLiOjHQ7GvnCafh+Z1EVGhD+MN8fLBIFmq4gUywL62c/pAB8k9pcB7meSDyKqNTeo2H5eF6CeoGgB+v3h/8AxHw7FExzcghmFNH1MZiVPoOrRVE2MpOLYVDGz7+ESVIzEZfW7QKlGYHQhtfqY5M3Itvi62HSFRVjGWtiUs22/frHks8zDxr5wPLXmOpOp+0TmTADVs3SnYQhhBUg6t0joBJGx/PCOhUBn+CzKQTi1VFYVcImVaHRSlxETSUzaFuKHXCpZYGG0strFXCUpyiLcTOSLRytKzrTpEjMBuY5UsQIhZJsYInLo2sNJvQpSrYFizpFmCSza9fwx4tEEyEsaftHTFUckpWM5CTdn3SaHxDs0FsbhIHSo/3FeHkg6h9KCC0Sejbl/taLcTLkUS63p4RNMgGhD+UFCUPlJPk3maHziuZLWbAA2qT6gD9YFGhuVnsvBq2cPpv9+n4C/wCXllJTdQuBoa7b9YGk4PEF3xKCMrJyoIKVakkqL6bQdgeF4lGV5yFJCeYkVWv+6lh07Vg4sfJHzP2wwnuiAzqUpwBqHqB4/WC/ZzAzyHUkN0VWv+/WPo3GPZiTi0ZVllCqFjQ6GMLw/B4jATZsqdMUsFlS81XGZiUvpVNNPGG4cI6CElklTDMBh8RKUSZSsjMWPNl3b7VvG64PwpC5QmpIUWyltGFi3h6Qi4Hwmfi8UpYxKhISAnKhgCSkZq6qzPXQWaPo8nh6ZMgSpQAAsIP18kmwlPg6Rkp/CnIKKMWNToX/AFMOeDcPZnFR9d93+8ApwWOK0HPKSkKV7wZXC0/KxdwbQ84cJ6X95LSamqFUKdCxq/SsRCNMMkrQZPRkD3gCbin18P3gnFzsxZj2sfJTGF0wNo2z/do2lZlGiS8T3bf/AFEM5apPiaxVLkN+fjRTjJ+UHlvb8MQUAT5h949WtpXyi0Jp93gWQokkk0dmt50/WCZqnFG9X84SGzAfxRlH3KSzhJqaVj55hVWAbtbu0bz+KajkQCKOdMwc6vprGDwaz8JA7lvD0jZLRk+w2UkZmfKm/MQxPeCZihlBOVunzfYQNPlgEVvpem7mJonKDMh07uwH3hUOyYSzFBvo7D7t1i8L/uDneBTKAZXw1u4bt2iXMASWLvlykxLKRekL6eLv9Y9geXjFNWniY6EMy+CRV4aoUaRKTw9tIv8A5U6QskW2aY5xihthMQwi6UcxvCyUFDSCpU0jQxzywS9G6zwHkuU2scoV/HERwQdMXLl6uDFQhXZE529FUuSXcQSUMfWkSRKrUwWiVoI1oxbDMJMLDmfcFiw7HWGCJGt+pr5fsIU4VJQaEU+Y2HQbn12FHhxLWGzVD6kVPYVYda+GlIhkvfpGhUfDyYFn6O8UYtCzQsgeJPrbxEXom/2htNz2H7esWmWD1tQbmw6noPE0MMBVhMHISrmUsEUcqNj2oCd+ukabByJLBsxDZbqI8awCiaE6JLXN+wT/AO2ujAEwSjH0LsG2Gu36Q46FJ2MJU1KXAGur3/DGZ9vpSZ8pCSGImJLpLLSPmao0bzFILGNWolKJZNqqOUA3FLneFXH+GzZ2XMWAUGCHYdSblqRvEya2bT2Vnolyky0pAQAEhtNK0h3iVIVe/wBIwvBJs+UBnRnDXSebo4N40eH4oFUBDjQhjtWB0xbRenDywpxOUCDqqh6H06wfIOWxKmvU/u3a3UQNJW5qgF/X0g1BAFAA/r0OxjKjSyC5iVP9CP0/WsBzwbuCPP1uPHyi+aWqK7jUffv5wFPnD5VMr+179joeh84GJFU6a1qbhq9/9QlM3Opy7d/WLMViCstMASx5SQQH07HqPKKfc1rlChVTag68tw+sZs1RdLTejhqakmKSrKoUUDbbzictV3q1OW/1gTGYkypZWqqQ5/yPhrCSBs+dfxOxiFYjKGOVLKZqH9YzuHGYBgD9XO8S41O98uZMqcynq7gCwsHpBWAFB6dI1ZmixeEBQGDnQCler6RBcpQDAhxWuvakFqkj4bE2Llt/GKgpJetdyKDzhIbAlAqFTahaxitOY0DEhvCDFDmoAQxqatFEtAAYivdvOE0NMrUuvwt3eOg+WsgByx6D9o6JpFWFiT0j33HSC48JjUgFEuJhHSLTHr9IBoOwCTli9BblJB8YG4UakVc7wxnStDTsIyaKs5GGerOdIIEkMxFNTv0B2jzDKHwk9qWEFS5RNz+gbdtodCsrEqgKhQfCmv3tbqd9YijOVb/nkAPSCZiX07R6mUBQeLa9B+V8oKCz1E75U03Udteyb9T6RLEYzKyACVKolIuAqlf8jR9gwtEkSWDhqtfU3A7D4j/2iLZeGKQ5HMpw9zW5J6uz9TFJE2LMTxApBKRRJZJtmX8y+wFu6TvFEjiyk0UhgGHpzHzp4QxxWFsdPhH3tcxCdggSbXO8JjQxwPGJTGoeGIxKCnQvGA4pwqYQchym9KWrDHA4OYAkKUolgXDMfPoTTpCU2NwRvJWJRanWLUykEuBWMtgV1bMSQSxDXYhiIZSZ6wzE+XqPSL5EOJqJTAN5dx+ekD4nHJDklqjN+hH59YTjGElsxc7MOn6mKZag71OZ36pLv41HjWG5C4hs7ib0QXULF+W3K52IsbeBBgCbK95UhlhypA1ahUkXpqnTtbzO1LhND1lqsR4n/wAhtEFuWyllpL5q1A1Ba4DeFdC+dlpElz8wylTbF261Jt3O9dxETFAspiA7EBq6gi4VoU6+RirGzQRnsUt7wAfCTTMG+QnyNNRAmExYdIzMpXwB6K/wLa7ai2zFBYRNYEFBd6hVGJDcp2LHUfvkvbziyRLMlxmOxY9K2HaHvFeIy5MtSyCUkBKgFAFKja1HuymY26R8y4ohSl5phz5uZKksErS5AJrQu4KdCCOsWkS2CS5HLbWvML9tobYWW4chtn9YERKNkpdzqXHlDPC0GUhnvTb0iWxpBEuTmBqyRc6n82EAIYk3o5s7CD5CWfK7EsANTA843ADHUDKPMamGgYtnpIJY3vZz4RQqjn6wViy5CQCB/wBIFesRXhmdNS+rgeVaiExo8kTuUPkHc1j2J/yJFlUjyABnNmgXMLsRxhCYz+M4muYWForl4Uk9YqxDqXx4GCpXFM1oSScNakaHgvDk/EKnaE2xoMwai71jUYcZ0Ajx1hWnAkB3KYN4epSFXcGjGEkDZZhaKLjr3+0M0qcbdNfz7QNjcOTzJipONDt9KU2/N4aAMWWrr9OsWYapqBStD9fQU3geTJMyrt6/SG+FSEpZ+zG/l+csNCbK1Ek0bzYKJ2PUx5NSqp+WzgEENcv+nWL20BNHOn+3rAq5ikmgoAxBLVNr28mpAwRSpBBck9A+m7kfWEvF0LmMApbOyilTHtTwhriMWakgmlQN68vyg/pWFiJ2UGgyiqgCKm+X4vCg8bRnJFpolgJKiaqpQEFn8Q2z1MWcKxVZktwyFEAoV8tDe1D9IIwK0pVUG9+qibv28HEWmTLzhixJzOAas4IO7kjzETwY+aL0TA+ooSDZ69OtfGCFThyvcVCh2ffUadIHWhklqXF3D5m8Br+V9UsJQFM9Q76G1dqjTvDpitBaMSb3pejXcGITAUqIAGuQPRvxopXLq7FJZ2FiLMWtp+CJEBrjShBcGxDfb9IdMVl2Hn5gnl+J5Z0UP7SoH/I3/wAYHRiOagqGqDtUXpqfsYgcWEJKqKqFEipB5g48006wq4lxlIUSHASoimodhY2/eLSJsce9yLGVNCk5X5k5TdCquRcNsHpCjjuNly+ZKQpw8vMxcPzJelQQRVvUQpXxNUwLSLD+ontZaWOuXm//ACaK8JJzkyyfjrLJPwzflfNbOOQ9Qgn4YaQrAcZiJkwmaFBxyzUKDoWkmiiNQbKr8TGhUGpkJSUsC0pRd3CjIWdSfmSWuBzJDtmQG8SsoctnBdK0G7WUnoWsdPCPCkoUyUpKbKdOUqSplCxdiGPQgagQxEVIUCQt3QSC9NWYNcQShOtQNWIb1iyZKCkkhaipIZKjdUsaKb5kO3YjQRLDzeQlJdhUgkfWIfZoujzEggOcwSevqwHqNoqUoBsqnHUfh84tMsFCmLu5B3IuGimQSEZkl2um8OhAM5IUSS5Gnf6R7KDllFSjdIJ+jGLZyDlKgWf4rsPAC8UyQFAaNqoKD/aEBCaFPb0A/WOj1cwAtmV4Fx5x0ACOThA3UQQFJobwjXi1XBjyViHNQ/i0aaIpm64QyzQdywf11jSSsKN26ENCL2YWgSxmSA+tjGkkYhi75k7m6fA6Qlsb0GSpRArX1iqfKBcg+B/aC0M/Xpb8/HijEppo+v48U4k2QkTnSQ1oXT0FwHYk2NR0v+VjkYlls9De8FSVBSw73fRvKkZtWWtDvByihApp2iydNrShHXb93gZWKyijMK32t6tFCZgV18QPCsUSMDOYOT4jv6wsx2PF3IV60qRzU3tFHEMVlSogkWNASbtsbwlxGM5aEmihlAIc0FTmO9m3gbGkEjHkqABKqitSWY1Hk1HoY9lTAVKQQ6F8yXoSakWbYbi+kJJJVy1c70ABBzZQdR8XZh0h1h5YUUv8qQACk0uCRqaAecJAEo+H4mVyqBZywrUnRimh0VcxchPKM1SnucrFLsfFwdKhjHstROQfEXoaDMgg5gRqTlZjvFiACXQo8vxC5ccyQ2o+INrTeKEeqWUUcgqd3sTc9nUX6uY4z5goGqwOZnHKeU76+h3i1Us2DHKSSSdEh2BNyzeBLxAYdnyBiSoMVUdJVbxY+ogoLOVxAhgQ7gJexBelBax8QIHxPETmJUHSpgGZnJDeIceRi4TARlAcVo7KJ+Jx1BJP5WspcsCS4FSGdjQsdbjw60KCxdjJ593MNQXSGD/5G3cGn3hLnUqauoIzKY3oTWnSttod42WVJOT+5zdmfLfrzFoHVNdkqDKe7dz9oGgBsBKIWFKIKbKLuyFDKrSlHivEhmzFlC5tUfEkkHlU7sbRauXlBcZSCUliyttKNrEMSoBSjbNU9Spi5GlT+aAE+KkK/qhIClgPmqnPUEg0uQq3TeF2U5QC6SmjF7VKa6h81eogiVNTkKXS2ajgnlULnoCmX5QNLQbFWQ2cMzBj1dmhDQZg15WPMA97gFtW0IoehivEycinTa+7p++h2IMeIVQIBCiCXLs4sHGl7dOsSzukhQDocAijpJfbf6mJodnoCiG6kgh6pNaaRQpZ6EpuwDeOx7QUMOpIdzkNKGg7hvykVywWYA16UIH+QgsAf3jqBAdrmg8zHmJYJzAgA0Iq42ZQcRfLlBJYv0Zq+LxSmRmU72qdD5Qux9EfdDWWCd3vHR4pVbpjyHQrMA0WYe4jo6K9C9n0PDKISGPy61+sOjLGUlmazU+l46OiV0OXZLDzSCACWr+sHTFlj2jo6NPRHsS4qhpt+ogzhcwlQeOjoz9lDOZrHqBQHU3846Oh+wAcQrmKaNQswvGemTlBSqm5G+nWPI6ExoKVKCc7D4QCnVi3WHGClAlSTUBRAck2CmjyOhoGFH/l9Sl9uZKiad/LSCZ6iACKEliehWhJ9FER0dFEs9Oo6G1LJUoHuDr4Wi2YPRZA7FBU3mT5x5HRRIPlGchrqL+SRfwiCBUjo+1WvHR0AC1SeYjdMt+vIn/2V5xQpRoNKitaMTr2EdHQmNC8LNKmjtXt948xyXSTqyT/AOCY6OhDBkFlqAsEhuj5DTo+kULU6q6mtBWkdHRPoYZNSEIJTQhTAjYu8Swyz7vM9aV/7Y6OgAJVSW4vQv1ILttaK8LUMbF3jo6JKRVITmBerAtAM5Z929HdrD6R0dAgYR7w/gEdHR0Mk//Z"
            sql_get_data="SELECT * FROM gps_data_user"
            con.execute(sql_get_data)
            fetch =con.fetchall()
            markers_1=[]
            for i  in fetch:
                data={
                      'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                      'lat': i[1],
                      'lng': i[2],
                      'infobox': "<h2><b><center>Marius(I3B4D)</center><br>Number:072345813</b></h2><br/><img src="+var_new+" width='100%' height='100%'>"
                     }
                markers_1.append(data)   


            connection_maps.commit()
    finally:
       connection_maps.close()
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        
        maptype="SATELLITE",
        markers=markers_1
    )

    return render_template('maps.html', mymap=mymap, sndmap=sndmap)


##@app.route('/admin_compose',methods=["POST","GET"])
##def admin_compose():
##    if request.method=="POST":
##        from_user=session['id']
##        target=request.form['target']
##        select_user="SELECT * FROM register WHERE email='"+str(target)+"'"
##        con.execute(select_user)
##        fetch=con.fetchone()
##        description=request.form['description']
##        messege=request.form['message']
##        title=request.form['title']
##        picture="hjjhvhjvjh"
##        if str(fetch[4])==str(target):
##             insert_into_notification="INSERT INTO notification VALUES('','"+str(fetch[0])+"','"+str(from_user)+"','"+str(description)+"','"+str(messege)+"','"+str(title)+"','"+str(picture)+"')"
##             con.execute(insert_into_notification)
##             return "succes"
##        else:
##             return "error"




@app.route('/learn_anatomy',methods=["POST","GET"])
def learn_anatomy():
     id=request.args['id']
     id13=session['id']
     connect=session['connect']
     if id13=="":
         return redirect(url_for('logout'))
##     if url=="":
##         return redirect(url_for('logout'))
     if id13==None :
         return redirect(url_for('logout'))
     if id==id13:
         return redirect(url_for('logout'))
     if request.args['connect'] != 'connect':
         return redirect(url_for('login'))
     if request.args['connect'] == '':
         return redirect(url_for('login'))
     if request.args['connect']=="" and request.args['id']=="" and session['connect']=="connect" and session['id']:  
        redirect(url_for('index',id=id13,connect=connect))

     select_anatomy_models="SELECT * FROM anatomy_models  "
     con.execute(select_anatomy_models)
     select_anatomy=con.fetchall()
     return render_template("learn_anatomy.html",select_anatomy=select_anatomy)
import html

@app.route('/models',methods=['POST','GET'])
def models():
##    request_limit_1=request.form['limit']
##    request_limit_2=request.form['start']
    select_anatomy_models="SELECT * FROM anatomy_models WHERE embed_or_not=1 ORDER BY id ASC LIMIT 2"
    con.execute(select_anatomy_models)
    select_anatomy=con.fetchall()
    return render_template('models.html',select_anatomy=select_anatomy)


@app.route('/load_books',methods=['POST','GET'])
def load_books():
    select_books="SELECT * FROM carti ORDER BY id DESC LIMIT 6"
    con.execute(select_books)
    select_books1=con.fetchall()
    return render_template('load_books.html',select_books1=select_books1)

@app.route('/upload_embed',methods=['POST','GET'])
def upload_embed():
    if request.method=="POST":
        name_embed=request.method["name_embed"]
        embed_models=request.method["embed_models"]
        insert="INSERT INTO anatomy_models VALUES('','"+str(name_embed)+"','"+str(embed_models)+"','','"+str(session['id'])+"','1')"
        con.execute(insert)
        return "Is in the DB!"


@app.route('/translate',methods=['POST','GET'])
def translate(trans):
    trans=request.args['select']
    if request.method=="POST":
        translator = Translator()
        translator.detect(trans)
        trnaslate_1=translator.translate(trans, dest='ja')
        return redirect(url_for("profile",id=id13,connect='connect',trnaslate_1=trnaslate_1.text))
    
@app.route('/search_index_anatomy',methods=['POST','GET'])
def show_anatomy():
    if request.method=="POST":
        search=request.form['searching']
        sql_search="SELECT * FROM anatomy_models WHERE  name LIKE '%"+str(search)+"%' LIMIT 20"
        conn=con.execute(sql_search)
        if conn==0:
            flash("nothing found")
        get=con.fetchall()
##        return redirect(url_for("index",medic=session['medic'],id=session['id'],connect='connect'))
        var = jsonify(get)
        print(var)
        return jsonify(result=get)
        print(result)


@app.route("/augument_reality",methods=["POST","GET"])
def augument_reality():
    model=request.args['model']
    print(model)
    sql="SELECT * FROM anatomy_models WHERE id='"+str(model)+"' "
    con.execute(sql)
    model=con.fetchall()  
    return render_template("ar.html",model=model)


@app.route('/books_to_show',methods=['POST','GET'])
def books_to_show():
    var_get_show=request.args['id_to_show']
    select_books="SELECT * FROM poze_carti_pagini  WHERE id_carte='"+var_get_show+"'"
    con.execute(select_books)
    select_books1=con.fetchall()
    return render_template("books.html",select_books1=select_books1)


@app.route('/quest_post_for_user',methods=['GET','POST'])
def quest_post_for_user():
##    if request.method=="POST":
        selected_post=request.form["selected_post"]
        ##textarea
        input_nr_ques_1=request.form["input_nr_ques_1"]
        ##input
        var_input_1=request.form["input1"]
        var_input_2=request.form["input2"]
        var_input_3=request.form["input3"]
        var_input_4=request.form["input4"]
        #checkbox
        ques_1=request.form.get("ques_1")
        ques_2=request.form.get("ques_2")
        ques_3=request.form.get("ques_3")
        ques_4=request.form.get("ques_4")
        if ques_1!=None:
            sql="INSERT INTO questions_post VALUES('','"+str(input_nr_ques_1)+"','"+str(var_input_1)+"','"+str(selected_post)+"','"+str(var_input_2)+"','"+str(var_input_3)+"','"+str(var_input_4)+"')"
        if ques_2!=None:
            sql="INSERT INTO questions_post VALUES('','"+str(input_nr_ques_1)+"','"+str(var_input_2)+"','"+str(selected_post)+"','"+str(var_input_1)+"','"+str(var_input_3)+"','"+str(var_input_4)+"')"
        if ques_3!=None:
            sql="INSERT INTO questions_post VALUES('','"+str(input_nr_ques_1)+"','"+str(var_input_3)+"','"+str(selected_post)+"','"+str(var_input_1)+"','"+str(var_input_2)+"','"+str(var_input_4)+"')"
        if ques_4!=None:
            sql="INSERT INTO questions_post VALUES('','"+str(input_nr_ques_1)+"','"+str(var_input_4)+"','"+str(selected_post)+"','"+str(var_input_1)+"','"+str(var_input_2)+"','"+str(var_input_3)+"')" 
##        sql="INSERT INTO questions_post VALUES('','12','12','12','123','2113','2313')" 
        con.execute(sql)
        return "Succes" 


            
@app.route('/send_user_points',methods=['POST','GET'])
def send_user_points():
        points=request.form['data2'] 
        id_post=request.args['id']
        search_noti="SELECT * FROM post_points_notifi WHERE id_post="+str(id_post)+" AND id_user="+str(session['id'])+""
        result_count=con.execute(search_noti)
        if result_count==0:
            select="INSERT INTO post_points_notifi VALUES('','"+str(id_post)+"','"+str(session['id'])+"','"+str(points)+"')"
            con.execute(select)               
            select="UPDATE register SET points=points+"+str(points)+" WHERE id="+str(session['id'])+""
            con.execute(select)
            sql="SELECT * FROM post_points_notifi WHERE id_user='"+str(session['id'])+"' ORDER BY id DESC "
            find_out=con.execute(sql)
            if find_out%5==0:
                sql="INSERT INTO tests VALUES('','"+str(session['id'])+"','172800','last_time_points+32')"
                find_test=con.execute(sql)    
         
            return "Good job you read the post!"
        else:
            return "Read it!"
        


@app.route('/upload_models',methods=['POST','GET'])
def upload_models():
    id=request.args['id']
    id13=session['id']
    i=0
    if 'file' in request.files:
        f = request.files['file']
        f2=request.files['file2']
        file_path2 = os.path.join('static/models_anatomy_3d/', werkzeug.secure_filename(f2.filename))
        file_path = os.path.join('static/models_anatomy_3d/', werkzeug.secure_filename(f.filename))
        exten=file_path[-3:]
        f.save(file_path)
        f2.save(file_path2)
        sql="INSERT INTO anatomy_models VALUES('','"+str("Atom")+"','"+str(file_path)+"','"+str(file_path2)+"','"+str(session['id'])+"','0')"
        con.execute(sql)
                 
             
    return redirect(url_for("user_profile",id=id13,connect='connect'))


@app.route("/books_page_upload",methods=["POST","GET"])
def books_page_upload():
##    if request.method=="POST":
        select_book=request.form["book_to_show"]
        text=request.form["description1_books"]
        sql="INSERT INTO poze_carti_pagini VALUES('','"+str(select_book)+"','"+str(text)+"')"
        con.execute(sql)
        return "Sent!"

            
    
@app.route('/back_nice',methods=["POST","GET"])
def back_nice():
    return render_template("particle_back.html")


 
@app.route("/")
def home():
    return render_template("home.html")



@app.route("/animation_disease",methods=["POST","GET"])
def animation_disease():
    data_succes=request.args["data_succes"]
##    stadiu=request.args["stadiu"]
    prediction=float(data_succes)*100
##    print(float(stadiu)*100)
    return render_template("animation_disease.html",data=prediction)



@app.route("/upload_your_back",methods=["POST","GET"])
def upload_your_back():
    id=request.args['id']
    id13=session['id']
    i=0
    if 'file' in request.files:
        f = request.files['file']
        file_path = os.path.join('../static/back_pic_design/', werkzeug.secure_filename(f.filename))
        exten=file_path[-3:]
        for i in ALLOWED_EXTENSIONS:
           if i==exten:
                f.save(file_path)
##                i=1
##               
##                sql="UPDATE register SET profile_pic='"+file_path2+"' WHERE id='"+str(id_general_user)+"'"
##                con.execute(sql)
                 
             
    return "uploaded"

@app.route("/send_user_msg_data",methods=["POST","GET"])
def send_user_msg_data():
    if request.method=="POST":
        chose=request.form["chose"]
        phone1=request.form["phone1"]
        phone2=request.form["phone2"]
        phone3=request.form["phone3"]
        sql="INSERT INTO phone_peoaple VALUES('','"+str(session['id'])+"','"+str(chose)+"','"+str(phone1)+"','"+str(phone2)+"','"+str(phone3)+"')"
        con.execute(sql)
        return "Send"


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))


@app.route("/questions_load_post",methods=['POST','GET'])
def questions_load_post():
     return render_template("questions_load_post.html")




@app.route("/chat_bot",methods=["POST","GET"])
def chat_bot():
    sql="SELECT profile_pic,uname FROM register WHERE id='"+str(session['id'])+"'"
    con.execute(sql)
    profile_pic=con.fetchall()
    return render_template("chat_bot.html",profile_pic=profile_pic)


@app.route("/second_chat_bot",methods=["POST","GET"])
def second_chat_bot():
    sql="SELECT profile_pic,uname FROM register WHERE id='"+str(session['id'])+"'"
    con.execute(sql)
    profile_pic=con.fetchall()
    return render_template("second_chat_bot.html",profile_pic=profile_pic)


@app.route("/evaluate_score_test",methods=["POST","GET"])
def evaluate_score_test():
    var12=0
    get_score= request.get["data"]
##    for in1 in get_score:
##        if str(in1)=='c':
##            var12+=1
##  
    print(get_score)
    return get_score


@app.route("/model_load",methods=['POST','GET'])
def model_load():
    get_model_id=request.args['model_to_show']
    con.execute("SELECT * FROM anatomy_models WHERE id='"+str(get_model_id)+"'")
    select=con.fetchall()
    return render_template("model_load.html",select=select)


@app.route("/listen_voice",methods=["POST","GET"])
def listen_voice():
    if request.method=="POST":
        var=request.form["play_this"]
        engine = pyttsx.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-50)
        engine.say(var)
        engine.runAndWait()
    return "finised"    



@app.route('/select_models_from_db',methods=["POST","GET"])
def select_models_from_db():
    id13=session['id']
    limit=request.args['limit']
    print(limit)
    start=request.args['start']
    print(start)
##    select="SELECT * FROM comments WHERE post_id="+str(31)+" ORDER BY id DESC LIMIT "+str(start)+","+str(limit)+""    
##    select="SELECT comments.post,comments.name,comments.post_id , register.id,register.profile_pic,comments.id,abonari.id_user,abonari.id_abonat ,( SELECT profile_pic FROM register WHERE abonari.id_abonat=register.id ) FROM comments,register,abonari WHERE abonari.id_abonat=comments.post_id AND register.id=abonari.id_user ORDER BY comments.id DESC LIMIT "+str(start)+","+str(limit)+" "
    connection_index=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True)
    try:
         with connection_index.cursor() as con:
            select="SELECT * FROM anatomy_models ORDER BY id DESC LIMIT "+str(start)+","+str(limit)+" "
            con.execute(select)
            fetch=con.fetchall()
            connection_index.commit()        
    finally:
         connection_index.close()
    json_fetch=str(jsonify(fetch))
    print(len(json_fetch))       
    return jsonify(fetch)



@app.route('/select_books_for_load1',methods=['POST','GET'])
def select_books_for_load1():
    id13=session['id']
    limit=request.args['limit']
    print(limit)
    start=request.args['start']
    print(start)
    connection_index=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True)
    try:
         with connection_index.cursor() as con:
            select="SELECT * FROM carti LIMIT "+str(start)+","+str(limit)+""
            con.execute(select)
            fetch=con.fetchall()
            connection_index.commit()        
    finally:
         connection_index.close()    
    return jsonify(fetch)


@app.route('/news_to_show',methods=["POST","GET"])
def news_to_show():            
    return render_template("news_to_show.html")

@app.route('/select_news',methods=["POST","GET"])
def select_news():
    get_limit_1=request.args['start_news']
    get_limit_2=request.args['finish']
    connection_index=pymysql.connect(host='localhost',use_unicode=True,charset="utf8",user='root',password='',db='savelives',autocommit=True)
    try:
         with connection_index.cursor() as con:
            select="SELECT news.id,news.id_user AS special_id_user,news.title,news.time,news.active,(SELECT profile_pic FROM register WHERE register.id=special_id_user) AS photo,news.data FROM news,register GROUP BY news.id ORDER BY id DESC LIMIT "+str(get_limit_1)+","+str(get_limit_2)+""
            con.execute(select)
            select1=con.fetchall()            
    finally:
         connection_index.close()
    return jsonify(select1)      



@app.route('/code_editor',methods=['POST','GET'])
def code_editor():
    get_url=request.args['id_editor_file']
    select="SELECT * FROM ai_files WHERE id='"+str(get_url)+"'"
    con.execute(select)
    data=con.fetchall()
##    data2 = open("static/A.I_folders/A.I_Bogdan333/index.py","w") 
##     
##    print(data2)

    return render_template('code_editor.html',get_url=data),##data2=data2)

@app.route('/design_ai_tabs',methods=['POST','GET'])
def design_ai_tabs():
    select="SELECT * FROM ai_files LIMIT 16"
    con.execute(select)
    select=con.fetchall()
    return render_template('design_ai_tab.html',select=select)


@app.route('/upload_news_data',methods=["POST","GET"])
def upload_news_data():
    if request.method=="POST":
        get_news_data=request.form['emit_data_news']
        news_title=request.form['news_title']
        sql="UPDATE news SET title='"+str(news_title)+"',data='"+str(get_news_data)+"' WHERE id_user='"+str(session['id'])+"'"
        con.execute(sql)
        return str()

import io

@app.route('/get_file_name',methods=['POST','GET'])
def get_file_name():
    if request.method=="POST":
        py_name=request.form['py_file_name']
        f= open(str(py_name)+".py","w+")
        for i in range(10):
             f.write("This is line %d\r\n" % (i+1))
        f.close()
        your_path="A.I_Bogdan333"
        path="static/A_I_folders/"+your_path+"/"+str(py_name)+".py"
        sql="INSERT INTO ai_files VALUES('','"+str(session['id'])+"','"+str(path)+"','Bogdan333','May 4','adadasdas')"
        con.execute(sql)
        return "Create!"



@app.route('/file_manager',methods=['POST','GET'])
def file_manager():
    return render_template('file_manager.html')

@app.route('/lateral_menu',methods=['POST','GET'])
def lateral_menu():
    return render_template("lateral_menu.html")


@socketio.on('connect', namespace='/bot')
def bot_connect():
    emit('my_response_bot', {'data': 'Connected','number':'1'})




@socketio.on('my_bot', namespace='/bot')
def bot(message):
    i=message['number']
    j=1
    user_questions=["help","number","take"]
    pages=["profile","learn_anatomy"]
    begin=["hey","hi","what's up","hello "]
    question=["what's yout question","say","hello I wait for your question"]
    bye_bot=["bye","bye my friend","I am happy that I helped you!","have a nice day","Good Luck!"]
    time_to_take=["One second...","One minute..."]
    response_special=response_chat_bot(message['data'])
    if message['data'][:6]=="search" or message['data'][:4]=="read" :
        word_to_show=message['data'].split()   
    engine1 = pyttsx.init()
    if message['number']==1: 
        a=random.choice(begin)
        emit('my_response_bot', {'data': a,'number':2})
##    if message['number']==2 and not(message['number'] in user_questions): 
##        a=random.choice(question)
##        emit('my_response_bot', {'data': a+"(if you need help type help)",'number':2}) 
   
##        emit('my_response_bot', {'data': a})
    if message['number']==2:
        if message['data'][:6]=="search":     
            emit('my_response_bot', {'data': show_search_data(word_to_show[1]),'number':2})
        if message['data'][:4]=="read":
            emit('my_response_bot', {'data': show_text_data(word_to_show[1]),'number':2})       
        if message['data']=="help" and message['number']==2:
            l='''
            take:'name_of_the_page'<br/>
            points
            <br/>calculate:'give_number_operation_number'<br/>
            pages
            <br/>bye
            <br/>bot
            <br/>search
            <br/>read
                       '''
            emit('my_response_bot', {'data': l})
            a=random.choice(question)
            emit('my_response_bot', {'data': a,'number':2})        
        if message['data'][:4]=="take" and message['number']==2:      
            if message['data'][5:]=="profile":
                a=random.choice(time_to_take)
                emit('my_response_bot', {'data': a})
                emit('my_response_bot', {'data': "profile"})
            if message['data'][5:]=="learn_anatomy":
                a=random.choice(time_to_take)
                emit('my_response_bot', {'data': a})
                emit('my_response_bot', {'data': "learn_anatomy"})
            if message['data'][3:]=="bot":
                a=random.choice(time_to_take)
                emit('my_response_bot', {'data': a})
                emit('my_response_bot', {'data': "bot"})   
        if message['data'][:5]=="pages" and message['number']==2:
                l='''
                  profile<br/>learn_anatomy<br/>                   
                       '''
                emit('my_response_bot', {'data': l})
                a=random.choice(question)
                emit('my_response_bot', {'data': a,'number':2})
        if message['data'][:6]=="points" and message['number']==2:
                sql="SELECT points FROM register WHERE id='"+str(session['id'])+"'"
                con.execute(sql)
                fetch=con.fetchall()
                for i in fetch:
                    l="You have "+str(i[0])+" points!"
                emit('my_response_bot', {'data': l})
                a=random.choice(question)
                emit('my_response_bot', {'data': a,'number':2})         
        if message['data'][:3]=="bye" and message['number']==2:
                l='''
                  profile<br/>learn_anatomy<br/>                   
                       '''
                a=random.choice(bye_bot)
                emit('my_response_bot', {'data': a,'number':2})
        if message['data'][:4]=="time":
##                engine1.setProperty('rate', rate-50)
##                engine1.say(response_special)
##                engine1.runAndWait()
                emit('my_response_bot', {'data': str(response_special),'number':2})
##        if message['data'][:6]=="search"        
##    if message['number']!=1:
            

           
##            emit('my_response_bot', {'data': str(response_special),'number':2})  
            

##    if message['data'][:4]=="calculate" and message['number']==2:      
##        if message['data'][5:]=="Profile":
##            emit('my_response_bot', {'data': "One second..."})            
        
##        a=random.choice(question)
##        emit('my_response_bot', {'data': a,'number':2})




















            
        ##    os.system("say '"+a+"'")
##            input_user=message
##            i=2
##            if i==2:
##                while i==2:
##                    a=random.choice(question)
##                    if j==1:
##                        emit('my_response_bot', {'data': a+"(if you need help type help)"}) 
##                        j=2
##                    else:   
##                        emit('my_response_bot', {'data': a})     
##                    input_user=message
##                    if str(input_user)=="help":
##                        l='''take <name_of_the_page>
##                                 calculate <give_number_operation_number>                    
##                               '''
##                        emit('my_response_bot', {'data': l}) 
##                        pass    
##                    if str(input_user)=="bye":
##                        a=random.choice(bye_bot)
##                        emit('my_response_bot', {'data': a}) 
##                        i=3
##            if i==3:
##                exit()
##       
      

    
if __name__=='__main__':
      app.secret_key="uhsd;iuasdf2f23rgvugersdfdsfsdfsdsdfswq2314123234124gergw["
      socketio.run(app,host='0.0.0.0',port=5000,debug=True)



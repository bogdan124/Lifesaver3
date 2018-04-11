import os
import random
import time
from gtts import gTTS


i=1
j=1
while i!=3:   
    if i==1: 
        begin=["hey","hi","what's up","hello user"]
        question=["what's yout question","say","hello I wait for your question"]
        bye_bot=["bye","bye my friend","I am happy that I helped you!","have a nice day","Good Luck!"]
        a=random.choice(begin)
        print(a)
        tts = gTTS(text=a, lang='en')
    ##    os.system("say '"+a+"'")
        input_user=raw_input("")
        i=2
        if i==2:
            while i==2:
                a=random.choice(question)
                if j==1:
                    print(a+"(if you need help type help)")
                    j=2
                else:   
                    print(a)     
                input_user=raw_input("")
                if str(input_user)=="help":
                    print('''take <name_of_the_page>
                             calculate <give_number_operation_number>                    
                           ''')
                    pass    
                if str(input_user)=="bye":
                    a=random.choice(bye_bot)
                    print(a)
                    i=3
        if i==3:
            exit()
   
                    
        

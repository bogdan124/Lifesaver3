##from chatterbot import ChatBot
##chatbot = ChatBot("Ron Obvious")
##from chatterbot.trainers import ListTrainer
##
##conversation = [
##    "Hello",
##    "Hi there!",
##    "How are you doing?",
##    "I'm doing great.",
##    "That is good to hear",
##    "Thank you.",
##    "You're welcome."
##]
##
##chatbot.set_trainer(ListTrainer)
##chatbot.train(conversation)
##response = chatbot.get_response("Good morning!")
##print(response)
from gtts import gTTS
import os



var= "Drogurile practic sunt simple substanțe care și-au găsit receptori în organismul nostru, care acționează prin grăbirea, încetinirea sau modificarea proceselor unui anumit organ.             </p>"
tts = gTTS(text=var, lang='ro')
tts.save("static/mp3_post/good1.mp3")
##os.system("mpg321 good.mp3")

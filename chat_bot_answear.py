from chatterbot import ChatBot

# Create a new chat bot named Charlie
chatbot = ChatBot(
    'Lifesaver',
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter"
    ],
    trainer='chatterbot.trainers.ListTrainer'
)
chatbot.train([
        "Hi, can I help you?",
        "Sure, I'd like to book a flight to Iceland.",
        "Your flight has been booked.",
        "ok",
        "nice",
        "where is Iceland"
    ])

def response_chat_bot(input1): 
    response = chatbot.get_response(input1)
    return response

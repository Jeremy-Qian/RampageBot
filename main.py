from nltk.chat.util import Chat, reflections


pairs = [
    (r"hi|hello", ["Hello!", "Hi there!"]),
    (r"my name is (.*)", ["Hello %1!"]),
    (r"what do you do ?|who are you", ["I chat with you."]),
    (r"quit", ["Bye!"])
]

chatbot = Chat(pairs, reflections)
chatbot.converse()
print("hi")
print("Who are you")

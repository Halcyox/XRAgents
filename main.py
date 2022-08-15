# Python program to translate
# speech to text and text to speech

import speech_recognition as sr
import pyttsx3
import time
from server_local import server
import mic
import os

# try:
server.restart()
print("Server restarted.")
# except:
#     pass

sessionID = 1
characterID = 1
server.initialize()
server.create_character("Avatar", "Avatar is a wise philosopher who understands the world in complex yet beautiful, meta-cognitive and cross-paradigmatic ways. He speaks with the eloquence of a great writer, weaving connections through networks of intricate ideas.")
server.create_session("Contemplations on Entities", "The following is an enlightening conversation between you and Avatar about the nature of artificial and biological entities, on the substance of souls, individuality, agency, and connection.", "1")

while(True):

    myText = mic.startListen()
    print(myText)
    # print("Did you say "+MyText)
    # SpeakText(MyText)

    response = server.get_response(myText, sessionID, characterID)
    # print(response["responseText"])
    # mic.speakText(response["responseText"])

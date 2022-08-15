# Python program to translate
# speech to text and text to speech

import speech_recognition as sr
import pyttsx3
import time
from server_module import server

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to
# speech
def speakText(command):
	
	# Initialize the engine
	engine = pyttsx3.init()
	engine.say(command)
	engine.runAndWait()
	
def startListen():
	try:
		with sr.Microphone() as source2:
			
			# wait for a second to let the recognizer
			# adjust the energy threshold based on
			# the surrounding noise level
			r.adjust_for_ambient_noise(source2, duration=1)
			
			#listens for the user's input
			print("Listening...")
			audio2 = r.listen(source2, timeout=3)
			
			# Using google to recognize audio
			MyText = r.recognize_google(audio2)
			MyText = MyText.lower()
			
			# myText = mic.listen()
			# print(myText)
			# # print("Did you say "+MyText)
			# # SpeakText(MyText)
			# response = server.get_response(myText)
			# speakText(response)

			return MyText
    
	except sr.RequestError as e:
		print("Could not request results; {0}".format(e))
		
	except sr.UnknownValueError:
		print("unknown value error")

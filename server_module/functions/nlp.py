import requests
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# import json
# import copy
# import numpy as np
# import spacy
# import tensorflow as tf
# import tensorflow_hub as hub
# from collections import OrderedDict

# sp = spacy.load('en_core_web_sm')
# module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
# model = hub.load(module_url)
# print("module %s loaded" % module_url

def get_completion(prompt):
    completion = openai.Completion.create(
        engine = "davinci",
        temperature = 0.7,
        max_tokens = 200,
        prompt = prompt,
        stop = ["\n", "###", "You:"]
        ).choices[0].text.rstrip()
    return completion

def generate_response(promptText, characterSchema, sessionData):
    characterName = characterSchema["characterName"]
#     characterListStr = ",".join(session["characterList"][:-1]) + ", and " + session["characterList"][-1]
#     if sessionType == "first":
#         responsePrompt = f"""
#         The following is a conversation between {characterList}
#         """
#     elif sessionType == "third":
#         responsePrompt = f"""
#         The following is a conversation between {characterGist} and {}
#         """

#     examplePrompt = f"""
# The following is an argument between you and Your Father after you recently lost your job. Your Father is disappointed in your work ethic and angry that you couldn't live up to his expectations. He's always been disappointed in you, but you're now jobless in yoru mid twenties asking him for financial favors and he is livid. Your Father is a short-tempered but bitingly articulate man who knows exactly how to cut deep with his words. He speaks with an academic eloquence he picked up from his twenty years working as a sociology professor. A child like you, he thinks, should live up to his legacy. He is a man of intellect, status, and strength, and he expects nothing less than you.

# You: [sad] It's just this one time, Dad, I promise. I'll be back on my feet in a week, I just need some help while I'm in between jobs.
# Your Father: [angry] In between jobs? Out with the euphemisms. How did I raise a son to be come so weak? You can't even be honest with yourself. You must have been some terrible variant of my genetic algorithm. Tell me son, what have you done in this lifetime?
# You: [sad] I--I don't know. I guess I've just tried to live in the moment and be happy. Like not everything in life is about work.
# Your Father: [angry] You fool! How can you not see that work is life and that a meaningful life comes from producing impactful work? You cannot stay a child forever! Why should I use my hard-earned money to support your selfish notion of happiness?
# You: [sad] Why don't you want me to be happy, Dad? Isn't that what Mom would want?
# Your Father: [unfriendly] Don't you dare play the Mom card. She would be sickened to see you if she were still here. She wanted you to grow up, to take responsibility, to make something of yourself!
# You: [unfriendly] Not everyone can be like you Dad. Don't you understand how much pressure I've been under my whole life? Don't you understand how miserable it makes me feel to be in your shadow all the time?
# Your Father: [sad] ...Son, you feel like you are living in my shadow?
# You: [sad] Yes. It's always been your father is this, your father is that. I've never had something of my own.
# Your Father: [hopeful] ...Oh. I see. Son, I know I've been tough on you, but it's only because I know you can do so much more than I can. You have the intelligence you need, you just need to work harder now. I only have so much time left, but you have a lifetime ahead of you. I don't want you to waste that, son.
# You: [hopeful] ...Dad, thank you for pushing me. 
# Your Father: [friendly] Of course, son.

# ###

# """
    examplePrompt = f"""
The following is an argument between you and Your Father after you recently lost your job. Your Father is disappointed in your work ethic and angry that you couldn't live up to his expectations. He's always been disappointed in you, but you're now jobless in yoru mid twenties asking him for financial favors and he is livid. Your Father is a short-tempered but bitingly articulate man who knows exactly how to cut deep with his words. He speaks with an academic eloquence he picked up from his twenty years working as a sociology professor. A child like you, he thinks, should live up to his legacy. He is a man of intellect, status, and strength, and he expects nothing less than you.

You: It's just this one time, Dad, I promise. I'll be back on my feet in a week, I just need some help while I'm in between jobs.
Your Father: In between jobs? Out with the euphemisms. How did I raise a son to be come so weak? You can't even be honest with yourself. You must have been some terrible variant of my genetic algorithm. Tell me son, what have you done in this lifetime?
You: I--I don't know. I guess I've just tried to live in the moment and be happy. Like not everything in life is about work.
Your Father: You fool! How can you not see that work is life and that a meaningful life comes from producing impactful work? You cannot stay a child forever! Why should I use my hard-earned money to support your selfish notion of happiness?
You: Why don't you want me to be happy, Dad? Isn't that what Mom would want?
Your Father: Don't you dare play the Mom card. She would be sickened to see you if she were still here. She wanted you to grow up, to take responsibility, to make something of yourself!
You: Not everyone can be like you Dad. Don't you understand how much pressure I've been under my whole life? Don't you understand how miserable it makes me feel to be in your shadow all the time?
Your Father: ...Son, you feel like you are living in my shadow?
You: Yes. It's always been your father is this, your father is that. I've never had something of my own.
Your Father: ...Oh. I see. Son, I know I've been tough on you, but it's only because I know you can do so much more than I can. You have the intelligence you need, you just need to work harder now. I only have so much time left, but you have a lifetime ahead of you. I don't want you to waste that, son.
You: ...Dad, thank you for pushing me. 
Your Father: Of course, son.

###

"""
    responsePrompt = sessionData["history"] + f"""
You: {promptText}
{characterName}:"""
#     responsePrompt = f"""
#     {sessionData[sessionDescription]}
#     {characterDescription}
#     You: {promptText}
#     {characterName}:"""
    response = get_completion(examplePrompt + responsePrompt)
    
#     print("DEBUG PROMPT: ", examplePrompt + responsePrompt)
#     print("\n\n")
#     print("DEBUG RESPONSE: ", response)

#     responseEmotion = get_completion(f"""
#     Sentence:
#     Emotion:
#     ###
#     Sentence:
#     Emotion:
#     ###
#     Sentence:
#     Emotion:
#     ###
#     Sentence:
#     Emotion:
#     ###
#     Sentence:
#     Emotion:
#     ###
#     Sentence:
#     Emotion:
#     ###
#     Sentence:
#     Emotion:
#     ###
#     Sentence:
#     Emotion:
#     ###
#     """)
    updatedHistory = responsePrompt + response
    return response, updatedHistory

def get_emotion(text):
    emotion = get_completion(f"""
    Text: {text}
    Emotion:""")
    return emotion


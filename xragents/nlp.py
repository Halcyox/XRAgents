import requests
import openai
import os
from dotenv import load_dotenv
import time
from log_calls import log_calls
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
import openai.error
def get_completion(prompt):
    """Send in a prompt and get a completion"""
    with open("prompt-from-nlp.py.{int(time.time())}.txt", "w") as f:
        f.write(prompt)
    return openai.Completion.create(
        engine = "davinci",
        temperature = 0.8,
        max_tokens = 150,
        prompt = prompt,
        frequency_penalty = 1.5,
        stop = ["\n", "###", "You:"]
        ).choices[0].text.rstrip()

def summarize(to_be_summarized):
    """Summarize a text"""
    summary = openai.Completion.create(
        engine = "text-davinci-003",
        temperature = 0.8,
        max_tokens = 600,
        prompt = "Summarize the following conversation into fewer than 600 tokens:\n"+ to_be_summarized,
        frequency_penalty = 1.9,
        stop = ["\n"]
        ).choices[0].text.rstrip()
    return summary

def get_emotion(text):
    """This function is supposed to act as sentiment analysis, but it doesn't work currently."""
    emotion = get_completion(f"""
    Text: {text}
    Emotion:""")
    return emotion


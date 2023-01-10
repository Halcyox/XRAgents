import os
import random

# This file has utility methods for directory creation, etc.

# A fake type language for shared ID generation for random tags
SomeSharedIdSpace = int

def next_session() -> SomeSharedIdSpace:
    # TODO: snowflakes
    return random.randint(0,2**64 -1)

def create_directory(directory, clear=True): # create a directory if it doesn't exist, with the option to clear it
    if not os.path.exists(directory):
        os.makedirs(directory)
    if clear:
        for filename in os.listdir(directory):
            pass
            #os.remove(os.path.join(directory, filename))

# The Script class holds the information for a script, actors, context, and lines.
class Script:
    def __init__(self, voice, emotion, lines):
        self.voice = voice
        self.emotion = emotion
        self.lines = lines

    def get_voice(self):
        return self.voice

    def get_emotion(self):
        return self.emotion

    def get_lines(self):    
        return self.lines

def format_xml(lang,name,text,style):
    return f"""\
<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="{lang}">
    <voice name="{name}">
        <mstts:express-as style="{style}">
            {text}
        </mstts:express-as>
    </voice>
</speak>
        """
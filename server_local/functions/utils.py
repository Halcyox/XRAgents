import os

# This file has utility methods for directory creation, etc.

def create_directory(directory, clear=True): # create a directory if it doesn't exist, with the option to clear it
    if not os.path.exists(directory):
        os.makedirs(directory)
    if clear:
        for filename in os.listdir(directory):
            os.remove(os.path.join(directory, filename))

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

# saves the db history into a file, takes a server and a sessionID as parameters
def save_history(server, sessionID,outputDir="recording/script_output/"):
    dirname = os.path.dirname(__file__)
    # get the history from the server
    history = server.get_history(sessionID)
    # get the path to the history file
    historyPath = os.path.join(dirname,f"../../{outputDir}", f"{str(sessionID)}_history.txt")
    # open the file
    historyFile = open(historyPath, "w")
    # write the history to the file
    historyFile.write(history)
    # close the file
    historyFile.close()


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
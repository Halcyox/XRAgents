
# Python program to translate
# Speech to text and text to speech
import sys, time, os

import halcyox
from halcyox import Character, Session, Avatar
from halcyox.functions import audio, utils
import pandas as pd

import typing
NUM_ACTORS = 2 # We can't get more than 5 without lagging usually, modify this if you want more actors in the USD scene

primPaths = ["/World/audio2face/PlayerStreaming"] # Make the primitive path references for the number of actors
for i in range(NUM_ACTORS-1):
    primPaths.append(f"/World/audio2face_{(i+1):02d}/PlayerStreaming")

VOICES = pd.read_csv("deps/streaming_server/resources/VoiceStyles.csv") # Read the available Microsoft Azure Voices
from dataclasses import dataclass

@dataclass
class SceneDescription:
    num_characters: int
    names: list[str]
    descs: dict[typing.Any,typing.Any]

def allocate_characters(num_characters:int,names:list[str],descriptions: list[str]) -> dict[str,Character]:
    if num_characters > NUM_ACTORS:
        raise Exception("Too many characters for the number of actors.")
    characters = {}
    for i in range(num_characters):
        characters[names[i]] = Character(names[i], desc=descriptions[i], id=0,
                                                   voice=VOICES.sample(n=1)["Voice"].iloc[0],
                                                   primitivePath=primPaths[i])
    return characters

def script_input(inputDir):
    """load all text files in the input directory into a list
    and generate a conversation using it and audio2face"""
    inputFiles = []
    for file in os.listdir(inputDir):
        if file.endswith(".txt"):
            inputFiles.append(os.path.join(inputDir, file))
    print(f"dbg:{inputFiles}")
    for index,file in enumerate(inputFiles):
        print(index,file)
        with open(file, 'r') as f:
            lines = f.readlines()
            nAIs(lines,index+1)

from contextlib import contextmanager
@contextmanager
def make_session(*args, **kwds):
    """makes sure a session's save history is always saved!"""
    resource = Session(*args, **kwds)
    try:
        yield resource
    finally:
        # Code to release resource, e.g.:
        resource.save_history()

def nAIs(lines,sessid=1):
    #######################
    utils.create_directory("scripts/output_audio/", False)
    utils.create_directory("scripts/output_text/", False)
    utils.create_directory("scripts/ai/")
    #######################

    # get the number of characters and their names
    characters = {}
    for line in lines:
        if ":" in line:
            name = line.split(":")[0]
            if name not in characters:
                characters[name] = 1
    characters = allocate_characters(len(characters),list(characters.keys()),["",""])

    with make_session(id=0,
        name="Contemplations on Entities",
        desc="The following is an enlightening conversation between you and Avatar about the nature of artificial and biological entities, on the substance of souls, individuality, agency, and connection.",
        ) as sess:

        # inform a server about our server someday

        for line in lines:
            if ":" in line:
                name = line.split(":")[0]
                text = line.split(":")[1]
                sess.animate(characters[name], charLine=text)

        sess.save_history(outputDir="scripts/output_text/")
        time.sleep(0.5)
        audio.concat_audio_single_directory("scripts/ai/",outputPath="scripts/output_audio/output_"+ str(time.time())+".wav") # the finished audio file is saved

def personPlusAi():
    """This is a basic conversation between you and an AI. Choose your session description and what characters you want."""
    avatar = Avatar
    with make_session(id=1,
        name="Contemplations on Entities",
        desc="The following is an enlightening conversation between you and Avatar about the nature of artificial and biological entities, on the substance of souls, individuality, agency, and connection.",
    ) as sess:
    # Create directories
        utils.create_directory("recording/output/", False) # Output should not be cleared
        utils.create_directory("recording/ai/") # Clears temporary files there
        utils.create_directory("recording/user/") # Clears temporary files there

        shouldntExit = True # conversation will loop until user wants to exit
        while shouldntExit: # Keeps looping and listening to the user and gets input from AI as long as "quit" is not said by user
            latest_record = audio.listen_until_quiet_again()
            print(latest_record.spoken_content)

            if(latest_record.spoken_content == "quit" or latest_record.spoken_content is None): # Trigger for ending convo, will then concatenate
                shouldntExit = False
                break

            latest_record.file_handle.close()
            response = sess.get_response(avatar, latest_record.spoken_content, primPaths[0])
            print("Conversation: " + response)

        # Save the audio files to the output directory
        #time.sleep(0.5) # time pause for audio files to be written properly (prevents error)
        audio.concat_audio_double_directory("recording/ai/", "recording/user/") # the finished audio file is saved
        audio.cleanup("recording/ai/", "recording/user/") # delete the temporary files


if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")
    personPlusAi()
    #dirname = os.path.dirname(__file__)
    #script_input(os.path.join(dirname,"scripts/input/"))
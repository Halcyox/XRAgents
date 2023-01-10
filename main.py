import sys, time, os
import pandas as pd
import typing
import random
from dataclasses import dataclass

from consolemenu import *
from consolemenu.items import *

import xragents
from xragents import setting, scene
from xragents import audio, utils, cast, simulator
from xragents.types import Character

#from xragents.scene import Scene

NUM_ACTORS = 2 # We can't get more than 5 without lagging usually, modify this if you want more actors in the USD scene

primPaths = ["/World/audio2face/PlayerStreaming"] # Make the primitive path references for the number of actors
for i in range(NUM_ACTORS-1):
    primPaths.append(f"/World/audio2face_{(i+1):02d}/PlayerStreaming")

VOICES = pd.read_csv("deps/streaming_server/resources/VoiceStyles.csv") # Read the available Microsoft Azure Voices

def allocate_characters(num_characters:int,names:list[str],descriptions: list[str]) -> dict[str,Character]:
    """Create all the characters inside of a list"""
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

    with scene.make_scene(id=0,
                    name="Contemplations on Entities",
                    description="The following is an enlightening conversation between you and Avatar about the nature of artificial and biological entities, on the substance of souls, individuality, agency, and connection.",
                    characters=list(characters.values()),
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


# Create the menu
menu = ConsoleMenu("XRAgents", "Simulator Root Menu")

def one_ai():

    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")
    watchTV = setting.InfiniteTelevision()

    simulator.personPlusAi(cast.Avatar)
    #dirname = os.path.dirname(__file__)
    #script_input(os.path.join(dirname,"scripts/input/"))

def two_ai():
    watchTV = setting.InfiniteTelevision()

    simulator.twoAiPlusPerson(cast.Avatar, cast.Unvatar)


# A FunctionItem runs a Python function when selected
one_ai_item = FunctionItem("Talk with an AI", one_ai)

two_ai_item = FunctionItem("Watch two AI talk together", two_ai)

# Once we're done creating them, we just add the items to the menu
menu.append_item(one_ai_item)
menu.append_item(two_ai_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()
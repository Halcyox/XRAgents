import pathlib
import sys, time, os
import pandas as pd
import typing
import random

import io

import xragents
from xragents import setting, scene
from xragents import audio, utils, cast
from xragents.types import Character

def personPlusAi(chr: Character):
    history = []
    """This is a basic conversation between you and an AI. Choose your session description and what characters you want."""
    with scene.make_scene(id=utils.next_session(),
                    name="Contemplations on Entities",
                    description=f"The following is an enlightening conversation between you and {chr.name} about the nature of artificial and biological entities, on the substance of souls, individuality, agency, and connection.",
                    characters=[chr],
                    ) as sess:
        # Create directories
        utils.create_directory("recording/output/", False) # Output should not be cleared
        utils.create_directory("recording/ai/") # Clears temporary files there
        utils.create_directory("recording/user/") # Clears temporary files there

        shouldntExit = True # conversation will loop until user wants to exit
        print(f"You are now talking with {chr.name}!")
        print(f"Conversation description: {sess.description}")
        print(f"{chr.name}: {chr.desc} ")
        while shouldntExit: # Keeps looping and listening to the user and gets input from AI as long as "quit" is not said by user
            latest_record = audio.listen_until_quiet_again() # Audio based user input
            #latest_record = audio.ListenRecord(io.BytesIO(), pathlib.Path("dummy_file.wav"), input("You: ")) # Text based user input
            #print(latest_record.spoken_content)

            if(latest_record.spoken_content == "quit" or latest_record.spoken_content is None): # Trigger for ending convo, will then concatenate
                shouldntExit = False
                break

            latest_record.file_handle.close()
            response = sess.make_speak(chr, chr.primitivePath)
            history.append(setting.DialogHistory(response))
            #print(f"{chr.name}: {response}")

        # Save the audio files to the output directory
        #time.sleep(0.5) # time pause for audio files to be written properly (prevents error)
        audio.concat_audio_double_directory("recording/ai/", "recording/user/") # the finished audio file is saved
        audio.cleanup("recording/ai/", "recording/user/") # delete the temporary files

        return history
    
def twoAiPlusPerson(chr1: Character, chr2: Character):
    history = []
    """This is a basic conversation between you and an AI. Choose your session description and what characters you want."""
    with scene.make_scene(id=utils.next_session(),
                    name="Contemplations on Entities",
                    description=f"The following is an entertaining convo between {chr1.name} and {chr2.name} about the nature of artificial and biological entities, on the substance of souls, individuality, agency, and connection.",
                    characters=[chr1, chr2],
                    ) as sess:
        # Create directories
        utils.create_directory("recording/output/", False) # Output should not be cleared
        utils.create_directory("recording/ai/") # Clears temporary files there
        utils.create_directory("recording/user/") # Clears temporary files there

        shouldntExit = True # conversation will loop until user wants to exit
        print(f"You are now talking with {chr1.name} and {chr2.name}!")
        print(f"Conversation description: {sess.description}")
        #print(f"{chr.name}: {chr.desc} ")
        while shouldntExit: # Keeps looping and listening to the user and gets input from AI as long as "quit" is not said by user
            latest_record = audio.listen_until_quiet_again() # Audio based user input
            #latest_record = audio.ListenRecord(io.BytesIO(), pathlib.Path("dummy_file.wav"), input("You: ")) # Text based user input
            #print(latest_record.spoken_content)

            if(latest_record.spoken_content == "quit" or latest_record.spoken_content is None): # Trigger for ending convo, will then concatenate
                shouldntExit = False
                break

            latest_record.file_handle.close()

            for chr in sess.characters:
                response = sess.make_speak(chr, chr.primitivePath)
                history.append(setting.DialogHistory(response))

            #print(f"{chr.name}: {response}")

        # Save the audio files to the output directory
        #time.sleep(0.5) # time pause for audio files to be written properly (prevents error)
        audio.concat_audio_double_directory("recording/ai/", "recording/user/") # the finished audio file is saved
        audio.cleanup("recording/ai/", "recording/user/") # delete the temporary files

        return history
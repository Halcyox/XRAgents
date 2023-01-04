from dataclasses import dataclass
import typing

from .types import Character
from .audio import *
from .scene import *

import ZODB, ZODB.FileStorage  # Database storage of objects

from ZODB.blob import Blob


#@dataclass
#class DialogRound:
#    """Unimplemented placeholder for more granular information about each dialog round"""
#    who_spoke: Character
#    what_they_said: str
#    mental_state_before_round: typing.Any
#    private_information: typing.Any

@dataclass
class DialogHistory:
    """A class for storing a single phrase said by a single agent"""
    dialog_history : str

@dataclass
class SettingDescription:
    """High level description of all of the scenes inside of an individual setting."""
    settingDesc : str
    pass

@dataclass
class InfiniteTelevision:
    """
    This file holds functions that allow for the user
    to listen to 'n' number of AIs talk about things.

    The user can also step in and break the fourth
    wall at any time under a chosen character.

    Current limit is 9 supported animation nodes
    However you can have unlimited text AI talking in a scene
    """
    characters_: list[Character]
    history: list[DialogHistory]
    setting_description: SettingDescription

    def __init__(self):
        

    def format_prompt(self) -> str:
        pass

    def n_convo(self, chars: list[Character], setting_description: SettingDescription): # Given a list of characters, have those characters talk to each other under a specific session description.
        pass

    def personPlusAi(self, chr: Character):
        """This is a basic conversation between you and an AI. Choose your session description and what characters you want."""
        with make_scene(id=next_session(),
                        name="Contemplations on Entities",
                        desc=f"The following is an enlightening conversation between you and {chr.name} about the nature of artificial and biological entities, on the substance of souls, individuality, agency, and connection.",
                        description = SettingDescription(1, [chr], {}),
                        ) as sess:
            # Create directories
            utils.create_directory("recording/output/", False) # Output should not be cleared
            utils.create_directory("recording/ai/") # Clears temporary files there
            utils.create_directory("recording/user/") # Clears temporary files there

            shouldntExit = True # conversation will loop until user wants to exit
            print(f"You are now talking with {chr.name}!")
            print(f"Conversation description: {sess.desc_}")
            print(f"{chr.name}: {chr.desc} ")
            while shouldntExit: # Keeps looping and listening to the user and gets input from AI as long as "quit" is not said by user
                #latest_record = audio.listen_until_quiet_again() # Audio based user input
                latest_record = audio.ListenRecord(audio.init_file_handle(), 0, input("You: ")) # Text based user input
                #print(latest_record.spoken_content)

                if(latest_record.spoken_content == "quit" or latest_record.spoken_content is None): # Trigger for ending convo, will then concatenate
                    shouldntExit = False
                    break

                latest_record.file_handle.close()
                response = sess.make_speak(chr, primPaths[0])
                self.history.append(DialogHistory(response))
                #print(f"{chr.name}: {response}")

            # Save the audio files to the output directory
            #time.sleep(0.5) # time pause for audio files to be written properly (prevents error)
            audio.concat_audio_double_directory("recording/ai/", "recording/user/") # the finished audio file is saved
            audio.cleanup("recording/ai/", "recording/user/") # delete the temporary files

    def get_history(self):
        """This will provide the history so far """
        return self.history



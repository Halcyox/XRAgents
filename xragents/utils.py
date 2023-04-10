import os
import random
from dataclasses import dataclass
# This file has utility methods for directory creation, etc.

# A fake type language for shared ID generation for random tags
SomeSharedIdSpace = int

def next_session() -> SomeSharedIdSpace:
    # TODO: snowflakes
    return random.randint(0,2**64 -1)

def create_directory(directory, clear=True):
    """Creates a file directory if one does not already exist, with the option to clear it."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    if clear:
        for filename in os.listdir(directory):
            pass
            #os.remove(os.path.join(directory, filename))

def create_audio_directories():
    """Create all audio directories."""
    create_directory("recording/output/", False) # Output should not be cleared
    create_directory("recording/ai/") # Clears temporary files there
    create_directory("recording/user/") # Clears temporary files there

@dataclass
class Script:
    """This is a script. It holds information for actors, context, and lines."""
    voice: str 
    emotion: str
    lines: list[str]

from dataclasses import dataclass
import typing
from typing import Optional
import enum

class NeuralTTSSelector(enum.Enum):
    TONY = "en-US-TonyNeural"
    GUY = "en-US-GuyNeural"
@dataclass
class Character:
    """This is a character, we can have multiple characters in a scene.
    Characters have names, id, descriptions, primitive path, and voice from TTS."""
    name: str
    id: int # uuid

    desc: str

    wiki_link: str = ""
    voice: NeuralTTSSelector = NeuralTTSSelector.TONY
    primitivePath: Optional[str] = None

    def __str__(self):
        return repr(self)
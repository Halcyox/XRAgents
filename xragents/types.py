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
    
    def azure_ssml(lang,name,text,style):
        """
        Azure Speech SDK SSML to modify the voice of the TTS.
        
        https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup"""
        #TODO:busted?
        return f"""\
    <speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="{lang}">
        <voice name="{name}">
            <mstts:express-as style="{style}">
                {text}
            </mstts:express-as>
        </voice>
    </speak>
            """
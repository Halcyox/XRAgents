from dataclasses import dataclass
import typing

from .types import Character
from .audio import *

import ZODB, ZODB.FileStorage  # Database storage of objects

from ZODB.blob import Blob

@dataclass
class DialogRound:
    who_spoke: Character
    what_they_said: str
    mental_state_before_round: typing.Any
    private_information: typing.Any

@dataclass
class SceneDescription:
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
    characters: list[Character]
    history: list[DialogRound]
    scene_description: SceneDescription

    def format_prompt(self) -> str:
        pass

    def n_convo(self, chars: list[Character], scene_description): # Given a list of characters, have those characters talk to each other under a specific session description.
        pass


KoolaidMan = Character("K-Hole", id=8888888,
                       desc="The Kool-Aid Man represents the user of the program containing the AI,  who has broken the fourth wall and has been inserted into the metanarrative.")


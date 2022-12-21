from dataclasses import dataclass
from .character import Character
import typing

@dataclass
class DialogRound:
    who_spoke: Character
    what_they_said: str
    mental_state_before_round: typing.Any
    private_information: typing.Any

@dataclass
class Sitcom:
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

    def format_prompt(self) -> str:
        pass
    
KoolaidMan = Character("K-Hole", id=8888888,
                        desc="The Kool-Aid Man represents the user of the program containing the AI,  who has broken the fourth wall and has been inserted into the metanarrative.")


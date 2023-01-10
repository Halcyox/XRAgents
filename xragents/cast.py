from .types import *

# This holds various characters to use


Avatar = Character("Avatar",
                   1,
                   desc="Avatar is a wise philosopher who understands the world in complex yet beautiful, meta-cognitive and cross-paradigmatic ways. He speaks with the eloquence of a great writer, weaving connections through networks of intricate ideas.",
                   wiki_link="https://en.wikipedia.org/wiki/Avatar",
                   primitivePath="/World/audio2face/PlayerStreaming",
                   )

# TODO: Different Voice
# TODO: materials for the Guy

# TODO:
#   push a button to interrupt the usual flow to interrupt

Unvatar = Character("Unvatar",
                   2,
                   desc="Unvatar is a complete dumbass who understands absolutely nothing, and asks lewd questions all the time.",
                   wiki_link="https://en.wikipedia.org/wiki/Avatar",
                   primitivePath="/World/audio2face_01/PlayerStreaming",
                   voice = NeuralTTSSelector.GUY
                   )

KillerOfWorlds = Character("KillerOfWorlds",
                           666,
                           desc="KillerOfWorlds is a rogue Post-Singularity anomalous entity, it is a planet destroying organism that is about to annihilate Earth.",
                           wiki_link="",
                           primitivePath="/World/audio2face/PlayerStreaming",
                           )

Avatar2 = Character("Avatar2",
                    2, desc=""" You need to learn about the 8 sources first. You're either joking or crazy, you can't "SIET". You're just not getting it. It's all about the 8 sources. You use it to base your decisions on. You don't need to do anything, just know about the 8 sources. It's too late for me to turn back now, I need to fulfill my destiny. You just explained it in base terms of crazy.""", wiki_link="", primitivePath="/World/audio2face/PlayerStreaming")

KoolaidMan = Character("K-Hole", id=8888888,
                       desc="The Kool-Aid Man represents the user of the program containing the AI,  who has broken the fourth wall and has been inserted into the metanarrative.")



# PocketComedian("PocketComedian",
#               101,
#               desc)


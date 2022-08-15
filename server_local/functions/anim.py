import os
import sys
# sys.path.append("C:\Users\phn431\AppData\Local\ov\pkg\deps\90af9be5c280a03ee647052b3591de9d\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server\test_client.py")

def animate(wavPath, primitivePath):
    # sys.path.append(r"C:\Users\phn431\AppData\Local\ov\pkg\deps\90af9be5c280a03ee647052b3591de9d\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server")
    # make sure to add streaming code into functions module
    command = fr"""cd F:\Omniverse\Library\deps\90af9be5c280a03ee647052b3591de9d\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server && python F:\Omniverse\Library\deps\90af9be5c280a03ee647052b3591de9d\exts\omni.audio2face.player\omni\audio2face\player\scripts\streaming_server\test_client.py {wavPath} {primitivePath}"""
    # python test_client.py {wavPath} {primitivePath}
    # """
    os.system(command)

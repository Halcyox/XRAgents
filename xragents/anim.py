import os
import sys
import subprocess

def animate(wavPath, primitivePath):
    """Starts streaming audio to A2F and does an animation RPC."""
    # make sure to add streaming code into functions module
    stream_Path = os.path.abspath(fr"./deps/streaming_server")
    stream_Client = os.path.abspath(fr"./deps/streaming_server/test_client.py")
    command = fr"""cd {stream_Path} && py {stream_Client} {wavPath} {primitivePath}"""
    # python test_client.py {wavPath} {primitivePath}
    # """
    #print(f"$ {command}")
    os.system(command)
    #print([os.path.join(stream_Path, stream_Client), wavPath, primitivePath])
    #subprocess.call([os.path.join(stream_Path, stream_Client), wavPath, primitivePath], cwd=stream_Path)
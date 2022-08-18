import os
import sys

def animate(wavPath, primitivePath):
    # make sure to add streaming code into functions module
    stream_Path = os.path.abspath(fr"./deps/streaming_server")
    stream_Client = os.path.abspath(fr"./deps/streaming_server/test_client.py")
    print(stream_Path)
    print(stream_Client)
    command = fr"""cd {stream_Path} && python {stream_Client} {wavPath} {primitivePath}"""
    # python test_client.py {wavPath} {primitivePath}
    # """
    os.system(command)

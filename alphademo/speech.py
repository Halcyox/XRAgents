from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, MediaStreamError
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay

import av
import whisper

wm = whisper.load_model("base.en")

async def speech_consume(track: MediaStreamTrack):
    while True:
        try:
            frame = await track.recv()
            samples = frame.resample(16000).to_ndarray()

            res = wm.transcribe(samples)
            print(f"User decided to say\t{res['text']}")
        except MediaStreamError:
            return
                                                                                 

def reload_model(which):
    wm = whisper.load_model("which")

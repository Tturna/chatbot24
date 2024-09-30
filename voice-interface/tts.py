import torch
from TTS.api import TTS
import sounddevice as sd
import soundfile as sf
import os

torch.set_warn_always(False)

TTS_OUTPUT_FILENAME = "tts-out.wav"

device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/en/ljspeech/vits").to(device)

if tts.is_multi_speaker:
    print("TTS is multi speaker")
    print(tts.speakers)
else:
    print("TTS is NOT multi speaker")

message = "Hello! This is my very own text-to-speech program."
amplitudes = tts.tts_to_file(message, file_path=TTS_OUTPUT_FILENAME)

print("playing TTS audio...")
data, fs = sf.read(TTS_OUTPUT_FILENAME, dtype='float32')  
sd.play(data, fs)
sd.wait()
os.remove(TTS_OUTPUT_FILENAME)


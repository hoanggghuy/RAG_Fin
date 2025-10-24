import whisper
import sounddevice as sd
import soundfile as sf
import os
from dotenv import load_dotenv
load_dotenv()
ffmpeg_path = os.getenv("FFMPEG_PATH")
whisper_size_model = os.getenv("WHISPER_SIZE_MODEL")
model = whisper.load_model(whisper_size_model)
class Generate_Voice:
    def __init__(self,filename:str,duration: int=5, sample_rate:int=16000):
        self.filename = filename
        self.duration = duration
        self.sample_rate = sample_rate
    def record_audio(self):
        audio =sd.rec(int(self.duration*self.sample_rate), samplerate=self.sample_rate,dtype="float32",channels=1)
        print("Start recording")
        sd.wait()
        sf.write(self.filename,audio,self.sample_rate)
        print("Finish recording")
    def gen_text_from_audio(self):
        self.record_audio()
        audio_file = self.filename if self.filename.endswith(".wav") else self.filename + ".wav"
        result = model.transcribe(audio=audio_file,language="en")
        return result["text"]



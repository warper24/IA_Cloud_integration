import torch
from transformers import pipeline

class Transcriber:
    def __init__(self):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = pipeline("automatic-speech-recognition",
                              "openai/whisper-medium.en",
                              torch_dtype=torch.float16,
                              device=device)

    def transcribe(self, audio_file):
        return self.model(audio_file, chunk_length_s=28, return_timestamps=True)

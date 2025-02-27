import torch
import os
from transformers import pipeline

class Transcriber:
    def __init__(self, model_name="openai/whisper-medium.en"):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.model = None  # Chargement différé pour économiser les ressources

    def load_model(self):
        """Charge le modèle uniquement lorsque nécessaire"""
        if self.model is None:
            dtype = torch.float16 if "cuda" in self.device else torch.float32
            self.model = pipeline("automatic-speech-recognition",
                                  model=self.model_name,
                                  torch_dtype=dtype,
                                  device=self.device)

    def validate_audio_file(self, audio_file):
        """Vérifie si l'extension du fichier audio est valide (seulement .wav accepté)"""
        if not audio_file.lower().endswith(".wav"):
            raise ValueError(f"Format non supporté : {audio_file}. Seuls les fichiers .wav sont acceptés.")

    def transcribe(self, audio_file):
        """Effectue la transcription d'un fichier audio"""
        self.validate_audio_file(audio_file)  # Vérifie le format avant de continuer
        self.load_model()  # Charge le modèle seulement si nécessaire

        try:
            result = self.model(audio_file, chunk_length_s=28, return_timestamps=True)
            return result
        except Exception as e:
            print(f"Erreur lors de la transcription : {e}")
            return None

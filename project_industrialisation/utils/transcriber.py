import torch
import os
from transformers import pipeline


class Transcriber:
    """
    Classe permettant la transcription d'un fichier audio en texte
    en utilisant le modèle OpenAI Whisper.
    """

    def __init__(self, model_name="openai/whisper-medium.en"):
        """
        Initialise le transcripteur.

        Params
        ------
        model_name:
            Nom du modèle utilisé pour la transcription.
        """
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.model = None  # Chargement différé pour économiser les ressources

    def load_model(self):
        """
        Charge le modèle de transcription uniquement lorsque nécessaire.
        """
        if self.model is None:
            dtype = torch.float16 if "cuda" in self.device else torch.float32
            self.model = pipeline(
                "automatic-speech-recognition",
                model=self.model_name,
                torch_dtype=dtype,
                device=self.device,
            )

    def validate_audio_file(self, audio_file):
        """
        Vérifie si le fichier audio est au bon format (seul .wav est accepté).

        Params
        ------
        audio_file:
            Chemin du fichier audio à vérifier.
        raises ValueError:
            Si le fichier n'est pas au format .wav.
        """
        if not audio_file.lower().endswith(".wav"):
            raise ValueError(
                f"""Format non supporté : {audio_file}.
                Seuls les fichiers .wav sont acceptés."""
            )

    def transcribe(self, audio_file):
        """
        Effectue la transcription d'un fichier audio .wav en texte.

        Params
        ------
        audio_file:
            Chemin du fichier audio à transcrire.
        Return
        ------
        result:
            Résultat de la transcription sous forme de dictionnaire
            ou None en cas d'erreur.
        """
        self.validate_audio_file(audio_file)
        self.load_model()

        try:
            result = self.model(audio_file, chunk_length_s=28,
                                return_timestamps=True)
            return result
        except Exception as e:
            print(f"Erreur lors de la transcription : {e}")
            return None

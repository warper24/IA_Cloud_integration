import ffmpeg
import os

class AudioExtractor:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.validate_file()  # Vérification du format avant d'aller plus loin
        self.extracted_audio = f"audio-{os.path.splitext(input_file)[0]}.wav"

    def validate_file(self):
        valid_extensions = {".mp4", ".wav"}
        file_extension = os.path.splitext(self.input_file)[1].lower()

        if file_extension not in valid_extensions:
            raise ValueError(f"Format non supporté : {file_extension}. Seuls les fichiers .mp4 et .wav sont acceptés.")

    def extract_audio(self) -> str:
        try:
            stream = ffmpeg.input(self.input_file)
            stream = ffmpeg.output(stream, self.extracted_audio)
            ffmpeg.run(stream, overwrite_output=True)
            print(f"Extraction réussie : {self.extracted_audio}")
            return self.extracted_audio
        except ffmpeg.Error as e:
            print(f"Erreur lors de l'extraction de l'audio : {e}")
            return None


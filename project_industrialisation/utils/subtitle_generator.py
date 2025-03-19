import os

class SubtitleGenerator:
    """
    Classe permettant de générer un fichier de sous-titres SRT et
    une transcription texte à partir d'une transcription contenant
    des segments temporels et du texte.
    """

    def __init__(self, input_video: str, transcription: dict):
        """
        Initialise l'objet SubtitleGenerator avec une vidéo
        et sa transcription associée.

        Params
        ------
        input_video:
            Chemin du fichier vidéo en entrée (ex: "uploads/input.mp4").
        transcription:
            Dictionnaire contenant les segments de transcription
            (ex: {"chunks": [{"timestamp": [start, end], "text": "..."}]}).
        """
        # On récupère uniquement le nom de fichier sans dossier ni extension
        base_name = os.path.splitext(os.path.basename(input_video))[0]
        
        # On place le .srt dans le dossier "outputs"
        os.makedirs("outputs", exist_ok=True)
        self.subtitle_file = os.path.join("outputs", f"{base_name}.srt")

        self.transcription = transcription

    @staticmethod
    def format_time(seconds: float) -> str:
        """
        Convertit un temps en secondes au format SRT (hh:mm:ss,ms).
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int(round((seconds - int(seconds)) * 1000))
        return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

    def generate_subtitles(self) -> tuple:
        """
        Génère un fichier de sous-titres SRT et un fichier brut de transcription.
        
        return:
            (srt_file, transcription_file)
            Chemins du fichier SRT généré et du fichier texte brut.
        """
        if "chunks" not in self.transcription:
            raise ValueError("La transcription ne contient pas de 'chunks' valides.")

        subtitle_text = []
        transcription_text = []

        for index, chunk in enumerate(self.transcription["chunks"]):
            if "timestamp" not in chunk or "text" not in chunk:
                continue  # Ignore les entrées invalides

            start, end = chunk["timestamp"]
            if start >= end:
                continue  # Évite les segments avec un mauvais timing

            segment_start = self.format_time(start)
            segment_end = self.format_time(end)
            
            subtitle_text.append(
                f"{index + 1}\n{segment_start} --> {segment_end}\n{chunk['text']}".strip()
            )
            transcription_text.append(chunk["text"])

        # Écriture du .srt dans self.subtitle_file
        self._write_file(self.subtitle_file, "\n".join(subtitle_text))

        # Génération du fichier texte brut (dans "outputs" également)
        base_srt = os.path.splitext(os.path.basename(self.subtitle_file))[0]  # ex: "input"
        transcription_file = os.path.join("outputs", f"{base_srt}_transcription.txt")
        self._write_file(transcription_file, "\n".join(transcription_text))

        return self.subtitle_file, transcription_file

    @staticmethod
    def _write_file(filename: str, content: str):
        """
        Écrit du contenu dans un fichier texte.
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

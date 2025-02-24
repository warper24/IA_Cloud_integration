import os
import ffmpeg

class VideoProcessor:
    def __init__(self, video_path, subtitles_path, output_path):
        """
        Classe pour ajouter des sous-titres directement à une vidéo.

        :param video_path: Chemin de la vidéo d'entrée.
        :param subtitles_path: Chemin du fichier de sous-titres (.srt ou .ass).
        :param output_path: Chemin du fichier vidéo de sortie.
        """
        self.video_path = video_path
        self.subtitles_path = subtitles_path
        self.output_path = output_path

    def add_subtitles(self):
        """ Ajoute des sous-titres incrustés directement dans la vidéo. """
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Vidéo introuvable : {self.video_path}")

        if not os.path.exists(self.subtitles_path):
            raise FileNotFoundError(f"Fichier de sous-titres introuvable : {self.subtitles_path}")

        # Vérifier si le fichier de sous-titres est en .srt
        file_extension = os.path.splitext(self.subtitles_path)[1].lower()
        if file_extension == ".srt":
            # Conversion en .ass pour assurer la compatibilité avec FFmpeg
            ass_subtitles_path = self.subtitles_path.replace(".srt", ".ass")
            self.convert_srt_to_ass(ass_subtitles_path)
        else:
            ass_subtitles_path = self.subtitles_path  # Si déjà en .ass, pas besoin de conversion

        # Ajout des sous-titres en utilisant FFmpeg
        try:
            ffmpeg.input(self.video_path).output(
                self.output_path, vf=f"subtitles={ass_subtitles_path}"
            ).run(overwrite_output=True)
            print(f"Vidéo sous-titrée générée : {self.output_path}")
        except ffmpeg.Error as e:
            print(f"Erreur lors de l'incrustation des sous-titres : {e}")

    def convert_srt_to_ass(self, ass_output_path):
        """ Convertit un fichier .srt en .ass pour une meilleure compatibilité avec FFmpeg. """
        try:
            ffmpeg.input(self.subtitles_path).output(ass_output_path).run(overwrite_output=True)
            self.subtitles_path = ass_output_path
            print(f"Conversion de {self.subtitles_path} en {ass_output_path} réussie.")
        except ffmpeg.Error as e:
            print(f"Erreur lors de la conversion des sous-titres : {e}")
            raise

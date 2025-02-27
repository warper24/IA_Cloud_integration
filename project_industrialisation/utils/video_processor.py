import os
import ffmpeg


class VideoProcessor:
    """
    Classe permettant d'ajouter des sous-titres
    incrustés directement dans une vidéo.
    """

    def __init__(self, video_path: str, subtitles_path: str, output_path: str):
        """
        Initialise le processeur vidéo.

        Params
        ------
        video_path:
            Chemin de la vidéo d'entrée.
        subtitles_path:
            Chemin du fichier de sous-titres (.srt ou .ass).
        output_path:
            Chemin du fichier vidéo de sortie.
        """
        self.video_path = video_path
        self.subtitles_path = subtitles_path
        self.output_path = output_path

    def validate_files(self):
        """
        Vérifie l'existence des fichiers vidéo et sous-titres.

        Return
        ------
        raises FileNotFoundError:
            Si un fichier est introuvable.
        """
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Vidéo introuvable : {self.video_path}")

        if not os.path.exists(self.subtitles_path):
            raise FileNotFoundError(
                f"Fichier de sous-titres introuvable :{self.subtitles_path}"
            )

    def add_subtitles(self):
        """
        Ajoute des sous-titres incrustés directement dans la vidéo.

        Return
        ------
        raises Exception:
            En cas d'erreur lors de l'incrustation des sous-titres.
        """
        self.validate_files()

        ass_subtitles_path = (
            self.convert_srt_to_ass()
            if self.subtitles_path.endswith(".srt")
            else self.subtitles_path
        )

        if not os.path.exists(ass_subtitles_path):
            raise FileNotFoundError(
                f"Fichier .ass introuvable après conversion :{ass_subtitles_path}"
            )

        try:
            ffmpeg.input(self.video_path).output(
                self.output_path, vf=f"subtitles={ass_subtitles_path}"
            ).run(overwrite_output=True)
            print(f"Vidéo sous-titrée générée : {self.output_path}")
        except Exception as e:
            print(f"Erreur lors de l'incrustation des sous-titres : {e}")
            raise

    def convert_srt_to_ass(self) -> str:
        """
        Convertit un fichier .srt en .ass pour une
        meilleure compatibilité avec FFmpeg.

        Return
        ------
        ass_output_path:
            Le chemin du fichier .ass généré.
        raises Exception:
            En cas d'erreur de conversion.
        """
        ass_output_path = self.subtitles_path.replace(".srt", ".ass")

        try:
            ffmpeg.input(self.subtitles_path, format="srt").output(
                ass_output_path, format="ass", **{"scodec": "ass"}
            ).run(overwrite_output=True)
            print(f"Conversion réussie : {self.subtitles_path} → {ass_output_path}")
            return ass_output_path
        except Exception as e:
            print(f"Erreur lors de la conversion des sous-titres : {e}")
            raise

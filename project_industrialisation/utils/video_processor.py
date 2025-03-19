import os
import ffmpeg

class VideoProcessor:
    """
    Classe permettant d'ajouter des sous-titres
    incrustés directement dans une vidéo (video_embedded)
    ou en tant que piste de sous-titres dans le conteneur MP4 (video_metadata).
    """

    def __init__(self, video_path: str, subtitles_path: str, output_path: str):
        self.video_path = video_path
        self.subtitles_path = subtitles_path
        self.output_path = output_path

    def validate_files(self):
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Vidéo introuvable : {self.video_path}")
        if not os.path.exists(self.subtitles_path):
            raise FileNotFoundError(f"Fichier de sous-titres introuvable : {self.subtitles_path}")

    def add_subtitles(self):
        """
        Ajoute des sous-titres incrustés (burned-in) dans la vidéo.
        """
        self.validate_files()
        
        ass_subtitles_path = (
            self.convert_srt_to_ass()
            if self.subtitles_path.endswith(".srt")
            else self.subtitles_path
        )
        
        out_dir = os.path.dirname(self.output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        if not os.path.exists(ass_subtitles_path):
            raise FileNotFoundError(f"Fichier .ass introuvable : {ass_subtitles_path}")

        try:
            video_path_ffmpeg = self.video_path.replace("\\", "/")
            ass_subtitles_path_ffmpeg = ass_subtitles_path.replace("\\", "/")
            output_path_ffmpeg = self.output_path.replace("\\", "/")

            print("Chemin vidéo :", self.video_path)
            print("Chemin sortie vidéo :", self.output_path)
            print("Chemin sous-titres .ass :", ass_subtitles_path)
            
            # Construction pas à pas de la commande
            cmd = ffmpeg.input(video_path_ffmpeg)
            cmd = cmd.output(
                output_path_ffmpeg,
                vf=f"subtitles={ass_subtitles_path_ffmpeg}"
            )
            cmd.run(overwrite_output=True)
            
            print(f"Vidéo sous-titrée générée : {self.output_path}")
        except Exception as e:
            print(f"Erreur lors de l'incrustation des sous-titres : {e}")
            raise

    def add_subtitles_metadata(self):
        """
        Ajoute les sous-titres en tant que piste distincte (mov_text) dans le conteneur MP4.
        """
        self.validate_files()

        # Création du dossier de sortie
        out_dir = os.path.dirname(self.output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        try:
            # Conversion des backslashs Windows en slashs
            video_path_ffmpeg = self.video_path.replace("\\", "/")
            subtitles_path_ffmpeg = self.subtitles_path.replace("\\", "/")
            output_path_ffmpeg = self.output_path.replace("\\", "/")

            print("Chemin vidéo :", self.video_path)
            print("Chemin sous-titres :", self.subtitles_path)
            print("Chemin sortie vidéo :", self.output_path)

            # Créez deux flux distincts pour la vidéo et les sous-titres
            video_input = ffmpeg.input(video_path_ffmpeg)
            subtitle_input = ffmpeg.input(subtitles_path_ffmpeg)

            # Passez les deux flux à ffmpeg.output() en utilisant un dictionnaire pour l'option -c:s
            ffmpeg.output(
                video_input,
                subtitle_input,
                output_path_ffmpeg,
                c='copy', **{"c:s": "mov_text"}
            ).run(overwrite_output=True)

            print(f"Sous-titres intégrés dans les métadonnées : {self.output_path}")
        except Exception as e:
            print(f"Erreur lors de l'ajout des sous-titres en métadonnées : {e}")
            raise



    def convert_srt_to_ass(self) -> str:
        ass_output_path = self.subtitles_path.replace(".srt", ".ass")
        ass_dir = os.path.dirname(ass_output_path)
        if ass_dir:
            os.makedirs(ass_dir, exist_ok=True)

        try:
            subtitles_path_ffmpeg = self.subtitles_path.replace("\\", "/")
            ass_output_path_ffmpeg = ass_output_path.replace("\\", "/")

            ffmpeg.input(subtitles_path_ffmpeg, format="srt").output(
                ass_output_path_ffmpeg, format="ass", scodec="ass"
            ).run(overwrite_output=True)

            print(f"Conversion réussie : {self.subtitles_path} → {ass_output_path}")
            return ass_output_path
        except Exception as e:
            print(f"Erreur lors de la conversion des sous-titres : {e}")
            raise

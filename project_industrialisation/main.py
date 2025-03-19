import sys
sys.path.insert(0, "C:/Users/aysim/Documents/Ynov/I.A. dans Cloud/j1/fil_rouge/IA_Cloud_integration/project_industrialisation")
from utils.audio_extractor import AudioExtractor
from utils.transcriber import Transcriber
from utils.subtitle_generator import SubtitleGenerator
from utils.video_processor import VideoProcessor
import os

def process_file(input_file: str, output_type: str, output_dir: str = "outputs") -> str:
    """
    Traite un fichier d'entrée (.mp4 ou .wav) et génère un résultat selon le type demandé.
    
    Paramètres:
      - input_file: Chemin vers le fichier d'entrée.
      - output_type: Type de résultat souhaité, parmi :
          * "video_embedded"   : Vidéo avec sous-titres incrustés
          * "video_metadata"   : Vidéo avec sous-titres en métadonnées
          * "subtitles"        : Sous-titres seuls (ex: .srt)
          * "text"             : Transcription textuelle brute
      - output_dir: Répertoire dans lequel sauvegarder le résultat.
    
    Retourne:
      - Le chemin du fichier généré.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    base_name, ext = os.path.splitext(input_file)
    ext = ext.lower()
    
    print(f"Fichier en entrée : {input_file} (extension : {ext})")

    # -- Étape 1 : Extraction + Transcription --
    if ext == ".mp4":
        print("Extraction de l'audio depuis la vidéo...")
        extractor = AudioExtractor(input_file)
        audio_file = extractor.extract_audio()
        print("Extraction réussie...")

        print("Transcription de l'audio...")
        transcriber = Transcriber()
        transcription = transcriber.transcribe(audio_file)
        print("Transcription réussie...")

        # Nettoyage du fichier audio temporaire, si besoin
        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)

    elif ext == ".wav":
        print("Fichier audio détecté, transcription directe...")
        transcriber = Transcriber()
        transcription = transcriber.transcribe(input_file)
        print("Transcription réussie...")

        # Impossibilité de créer une vidéo depuis un fichier audio
        if output_type in ["video_embedded", "video_metadata"]:
            raise ValueError("Impossible de générer une vidéo à partir d'un fichier audio.")
    else:
        raise ValueError("Format de fichier non supporté. Veuillez fournir un fichier .mp4 ou .wav")

    if not transcription:
        raise RuntimeError("La transcription a échoué ou est vide.")

    # -- Étape 2 : Génération des sous-titres si besoin --
    subtitles_file = None
    transcription_file = None

    if output_type in ["video_embedded", "video_metadata", "subtitles"]:
        print("Génération des sous-titres...")
        subtitle_generator = SubtitleGenerator(input_file, transcription)
        subtitles_file, transcription_file = subtitle_generator.generate_subtitles()
        print("Génération réussie...")

    # -- Étape 3 : Traitement selon le type de sortie --
    # 1) Vidéo avec sous-titres incrustés
    if ext == ".mp4" and output_type == "video_embedded":
        output_video = os.path.join(output_dir, f"{os.path.basename(base_name)}_embedded.mp4")
        print("Incrustation des sous-titres dans la vidéo...")
        processor = VideoProcessor(input_file, subtitles_file, output_video)
        processor.add_subtitles()
        print("VideoProcess réussie...")

        # Optionnel : on peut supprimer le fichier .srt après usage
        if subtitles_file and os.path.exists(subtitles_file):
            os.remove(subtitles_file)

        return output_video

    # 2) Vidéo avec sous-titres en métadonnées
    elif ext == ".mp4" and output_type == "video_metadata":
        output_video = os.path.join(output_dir, f"{os.path.basename(base_name)}_metadata.mp4")
        print("Ajout des sous-titres dans les métadonnées de la vidéo (piste de sous-titres).")
        print(input_file, subtitles_file)
        processor = VideoProcessor(input_file, subtitles_file, output_video)
        processor.add_subtitles_metadata()
        print("VideoProcess réussie...")

        # Optionnel : supprimer le .srt
        if subtitles_file and os.path.exists(subtitles_file):
            os.remove(subtitles_file)

        return output_video

    # 3) Sous-titres seuls
    elif output_type == "subtitles":
        if subtitles_file and os.path.exists(subtitles_file):
            return subtitles_file
        else:
            raise RuntimeError("Le fichier de sous-titres n'a pas été généré correctement.")

    # 4) Transcription texte brute
    elif output_type == "text":
        if "chunks" not in transcription:
            raise ValueError("La transcription ne contient pas de segments 'chunks'.")
        
        # On reconstruit le texte
        text_content = []
        for chunk in transcription["chunks"]:
            if "text" in chunk:
                text_content.append(chunk["text"])
        
        output_text = os.path.join(output_dir, f"{os.path.basename(base_name)}_transcript.txt")
        print("Enregistrement de la transcription en fichier texte...")
        with open(output_text, "w", encoding="utf-8") as f:
            f.write("\n".join(text_content))
        
        return output_text

    else:
        raise ValueError("Type de résultat demandé non supporté ou inconnu.")


# Pour test en ligne de commande
if __name__ == "__main__":
    try:
        # Exemple : traiter un fichier MP4 pour y ajouter des sous-titres en métadonnées
        result = process_file("input.mp4", "video_metadata")
        print("Résultat généré :", result)
    except Exception as e:
        print("Erreur lors du traitement :", str(e))

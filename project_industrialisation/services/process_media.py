import os
import shutil
import time
import logging
import subprocess
from utils.audio_extractor import AudioExtractor
from utils.transcriber import Transcriber
from utils.subtitle_generator import SubtitleGenerator
from utils.video_processor import VideoProcessor

# Configuration des logs
logging.basicConfig(filename="logs.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_process(message):
    logging.info(message)
    print(message)

# Chargement unique du modèle
transcriber = Transcriber()
transcriber.load_model()

def convert_srt_to_ass(srt_path):
    """
    Convertit un fichier .srt en .ass avec FFmpeg.
    """
    ass_output_path = srt_path.replace(".srt", ".ass")

    try:
        cmd = [
            'ffmpeg', '-y',
            '-f', 'srt', '-i', srt_path,
            '-c:s', 'ass', ass_output_path
        ]

        print(f"🔄 Commande de conversion SRT -> ASS : {' '.join(cmd)}")
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        if not os.path.exists(ass_output_path):
            raise FileNotFoundError(f"Le fichier ASS n'a pas été généré : {ass_output_path}")

        print(f"✅ Conversion réussie : {ass_output_path}")
        return ass_output_path

    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la conversion des sous-titres : {e}")
        print(f"Sortie d'erreur FFmpeg : {e.stderr}")
        raise

    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        raise

async def process_media_pipeline(file, is_video, generate_txt, generate_srt, generate_video):
    """
    Pipeline de traitement pour l'audio et la vidéo.
    
    - `is_video`: bool (True = Vidéo, False = Audio seul)
    - `generate_txt`: bool (Générer un fichier .txt ?)
    - `generate_srt`: bool (Générer un fichier .srt ?)
    - `generate_video`: bool (Générer une vidéo avec sous-titres ?)
    """
    safe_filename = file.filename.replace(" ", "_").replace("(", "").replace(")", "")
    input_path = f"uploads/{safe_filename}"
    output_path = f"outputs/output_{safe_filename}"
    
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("audio-uploads", exist_ok=True)
    os.makedirs("sub-uploads", exist_ok=True)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    log_process(f"📥 Fichier reçu : {input_path}")
    start_time = time.time()

    try:
        # 1️⃣ EXTRACTION AUDIO
        if is_video:
            extractor = AudioExtractor(input_path)
            extracted_audio = extractor.extract_audio()
        else:
            extracted_audio = input_path  # Si c'est déjà un fichier audio, on l'utilise directement

        log_process(f"🎵 Audio extrait : {extracted_audio}")

        # 2️⃣ TRANSCRIPTION AUDIO (si TXT ou SRT demandés)
        transcription = None
        transcript_file = None
        if generate_txt or generate_srt:
            transcription = transcriber.transcribe(extracted_audio)
            log_process("📝 Transcription terminée")

            if generate_txt:
                transcript_file = f"outputs/{safe_filename}.txt"
                with open(transcript_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(chunk["text"] for chunk in transcription["chunks"]))
                log_process(f"✅ Fichier texte généré : {transcript_file}")

        # 3️⃣ GÉNÉRATION DES SOUS-TITRES (SRT si demandé)
        subtitle_file = None
        if generate_srt:
            subtitle_generator = SubtitleGenerator(input_path, transcription)
            subtitle_file, _ = subtitle_generator.generate_subtitles()
            log_process(f"✅ Fichier SRT généré : {subtitle_file}")

        # 4️⃣ INCRUSTATION DES SOUS-TITRES (si vidéo demandée)
        if is_video and generate_video and subtitle_file:
            ass_subtitles_path = convert_srt_to_ass(subtitle_file) if subtitle_file.endswith(".srt") else subtitle_file
            processor = VideoProcessor(input_path, ass_subtitles_path, output_path)
            processor.add_subtitles()
            log_process(f"✅ Vidéo sous-titrée générée : {output_path}")

        end_time = time.time()
        log_process(f"📌 Traitement terminé en {end_time - start_time:.2f} secondes")

        # Retourner uniquement les fichiers générés
        result = {"message": "Traitement terminé"}
        if transcript_file:
            result["transcription_file"] = transcript_file
        if subtitle_file:
            result["subtitle_file"] = subtitle_file
        if is_video and generate_video and subtitle_file:
            result["output_video"] = output_path

        return result

    except Exception as e:
        log_process(f"❌ Erreur lors du traitement : {str(e)}")
        return {"error": str(e)}

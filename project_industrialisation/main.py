from utils.audio_extractor import AudioExtractor
from utils.transcriber import Transcriber
from utils.subtitle_generator import SubtitleGenerator
from utils.video_processor import VideoProcessor

def main():
    input_video = "input.mp4"
    output_video = "output.mp4"

    # Extraction audio
    extractor = AudioExtractor(input_video)
    extracted_audio = extractor.extract_audio()

    # Transcription
    transcriber = Transcriber()
    transcription = transcriber.transcribe(extracted_audio)

    # Génération des sous-titres
    subtitle_generator = SubtitleGenerator(input_video, transcription)
    subtitle_file, transcription_text = subtitle_generator.generate_subtitles()

    # Ajout des sous-titres à la vidéo
    processor = VideoProcessor(input_video, subtitle_file, output_video)
    processor.add_subtitles()

    print(f"Transcription terminée.\nVidéo : {output_video}\nSous-titres : {subtitle_file}\nTranscription : transcription.txt")
    
if __name__ == "__main__":
    main()

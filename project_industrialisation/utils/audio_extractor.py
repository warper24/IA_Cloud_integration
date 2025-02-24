import ffmpeg

class AudioExtractor:
    def __init__(self, input_video):
        self.input_video = input_video
        self.extracted_audio = f"audio-{input_video.replace('.mp4', '')}.wav"

    def extract_audio(self):
        stream = ffmpeg.input(self.input_video)
        stream = ffmpeg.output(stream, self.extracted_audio)
        ffmpeg.run(stream, overwrite_output=True)
        return self.extracted_audio

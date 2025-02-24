import math

class SubtitleGenerator:
    def __init__(self, input_video, transcription):
        self.input_video_name = input_video.replace(".mp4", "")
        self.subtitle_file = f"sub-{self.input_video_name}.srt"
        self.transcription = transcription

    def format_time(self, seconds):
        hours = math.floor(seconds / 3600)
        seconds %= 3600
        minutes = math.floor(seconds / 60)
        seconds %= 60
        milliseconds = round((seconds - math.floor(seconds)) * 1000)
        seconds = math.floor(seconds)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def generate_subtitles(self):
        text = ""
        transcription_text = ""
        offset = 0

        for index, chunk in enumerate(self.transcription["chunks"]):
            start = offset + chunk["timestamp"][0]
            end = offset + chunk["timestamp"][1]

            if start > end:
                offset += 28
                continue

            segment_start = self.format_time(start)
            segment_end = self.format_time(end)
            text += f"{index + 1}\n{segment_start} --> {segment_end}\n{chunk['text']}\n\n"
            transcription_text += chunk["text"] + "\n"

        with open(self.subtitle_file, "w") as f:
            f.write(text)

        with open("transcription.txt", "w") as f:
            f.write(transcription_text)

        return self.subtitle_file, "transcription.txt"

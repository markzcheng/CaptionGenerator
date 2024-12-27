from moviepy import VideoFileClip
import whisper
import pysrt
import tkinter as tk
from tkinter import scrolledtext
from Editor import CaptionEditor

# video_path = input path for where video is stored
# audio_path = output path for where the audio will be stored
def extract_audio(video_path, audio_path):
   try:
       video = VideoFileClip(video_path)
       video.audio.write_audiofile(audio_path)
       print(f"Audio successfully extracted to: {audio_path}")
   except Exception as e:
       print(f"An error occurred: {e}")

def transcribe_audio(audio_path, model_size="base"):
   model = whisper.load_model(model_size)
   result = model.transcribe(audio_path)
   print("Transcription complete.")
   return result["text"], result["segments"]

def save_as_srt(segments, output_path):
   subs = pysrt.SubRipFile()
   for i, segment in enumerate(segments):
       start_time = segment["start"]
       end_time = segment["end"]
       text = segment["text"]
       sub = pysrt.SubRipItem(
           index=i+1,
           start=seconds_to_subrip_time(start_time),
           end=seconds_to_subrip_time(end_time),
           text=text
       )
       subs.append(sub)
   subs.save(output_path, encoding='utf-8')
   print(f"Subtitles saved to: {output_path}")

def seconds_to_subrip_time(seconds):
   hours = int(seconds // 3600)
   minutes = int((seconds % 3600) // 60)
   secs = int(seconds % 60)
   milliseconds = int((seconds - int(seconds)) * 1000)
   return pysrt.SubRipTime(hours=hours, minutes=minutes, seconds=secs, milliseconds=milliseconds)

def video_to_captions(video_path, audio_path, srt_path):
   extract_audio(video_path, audio_path)
   transcription, segments = transcribe_audio(audio_path)
   save_as_srt(segments, srt_path)

def run_gui():
    root = tk.Tk()
    root.title("Caption Editor")
    app = CaptionEditor(root)

    # menu_bar = tk.Menu(root)
    # file_menu = tk.Menu(menu_bar, tearoff=0)
    # file_menu.add_command(label="Open", command=app.open_file)
    # file_menu.add_command(label="Save", command=app.save_file)
    # menu_bar.add_cascade(label="File", menu=file_menu)
    # root.config(menu=menu_bar)

    root.mainloop()

def main():
   video_path = "Videos/Test.mp4"
   output_audio_path = "Audios/output_audio.wav"
   srt_path = "Captions/captions.srt"
   video_to_captions(video_path, output_audio_path, srt_path)
   run_gui()

if __name__ == "__main__":
   main()
from openai import OpenAI
from moviepy.editor import AudioFileClip
from pathlib import Path
import os


class Lecture():
  """ 
  Class to represent a lecture audio file and its transcription.
  """
  def __init__(self, audio_file: str, split_list: list, client: OpenAI):
    self.audio_file = audio_file
    
    if('.mp4' in audio_file):
      audio_path = Path(audio_file)
      file_stem = audio_path.stem
      self.audio_file = self.__mp4_to_mp3(audio_file, f"{file_stem}.mp3")
      
    audio_path = Path(audio_file)
    self.audio_size = (os.stat(audio_path).st_size / (1024 * 1024))
    self.split_list = split_list
    self.client = client
    self.transcription = ""
    self.notes = ""
    print(self.audio_file)
 
  def __mp4_to_mp3(self, mp4: str, mp3: str):
    file = AudioFileClip(mp4)
    file.write_audiofile(mp3)
    file.close()
    return mp3

  def transcribe_audio(self) -> str:
    if self.split_list != []:
      for f in self.split_list:
        audio_file = open(f, "rb")
        self.transcription += self.client.audio.transcriptions.create(
          model="whisper-1", 
          file=audio_file,
          response_format="text",
        ) + " "
    else:
      audio_file = open(self.audio_file, "rb")
      self.transcription += self.client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text",
      )
    return self.transcription

  def take_notes(self) -> str:
    response = self.client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a college student taking notes for a lecture in Markdown formatting. Be detailed in your notes to avoid later confusion."},
      {"role": "user", "content": self.transcription},
    ])
    self.notes = response.choices[0].message.content
    return self.notes
  
  def get_notes(self) -> str:
    return self.notes
  
  def get_transcription(self) -> str:
    return self.transcription
  
  def get_audio_file(self) -> str:
    return self.audio_file
  
  def get_audio_size(self) -> float:
    return self.audio_size

  def set_split_list(self, split_list: list):
    self.split_list = split_list
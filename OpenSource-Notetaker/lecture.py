from moviepy.editor import AudioFileClip
from pathlib import Path
import os
import whisper


class Lecture():
  """ 
  Class to represent a lecture audio file and its transcription.
  """
  def __init__(self, audio_file: str, split_list: list = [], client: str = "medium.en"):
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
    self.model = whisper.load_model(client)
 
  def __mp4_to_mp3(self, mp4: str, mp3: str) -> str:
    file = AudioFileClip(mp4)
    file.write_audiofile(mp3)
    file.close()
    return mp3

  def transcribe_audio(self) -> str:
    result = self.model.transcribe(self.audio_file)
    self.transcription = result["text"]
    return self.transcription

  def take_notes(self) -> str:
    """Implement this function to take notes from the lecture transcription using an open source model like Phi-3, ollama, or something else."""
    # TODO: Implement this function
    # TODO: Figure out how to install flash attention (or switch to Ubuntu and try there)
    return ""
  
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
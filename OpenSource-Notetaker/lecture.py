from moviepy.editor import AudioFileClip
from pathlib import Path
import os
from whisper import Whisper
from transformers import Pipeline


class Lecture():
  """ 
  Class to represent a lecture audio file and its transcription.
  """
  def __init__(self, whisper_client: Whisper, llm_pipeline: Pipeline, audio_file: str, split_list: list = [], ):
    self.audio_file = audio_file
    
    if('.mp4' in audio_file):
      audio_path = Path(audio_file)
      file_stem = audio_path.stem
      self.audio_file = self.__mp4_to_mp3(audio_file, f"{file_stem}.mp3")
      
    audio_path = Path(audio_file)
    self.audio_size = (os.stat(audio_path).st_size / (1024 * 1024))
    self.split_list = split_list
    self.whisper = whisper_client
    self.transcription = ""
    self.notes = ""
    self.llm = llm_pipeline
 
  def __mp4_to_mp3(self, mp4: str, mp3: str) -> str:
    file = AudioFileClip(mp4)
    file.write_audiofile(mp3)
    file.close()
    return mp3

  def __split_prompt(self) -> list:
    splt = self.transcription.split()
    split = []
    lst = []
    for i in range((len(splt) // 400)+1):
      if (i*400)+400 >= len(splt):
        lst.append(splt[(i*400):-1])
      else:
        lst.append(splt[(i*400):(i*400)+400])
    for block in lst:
      s = ""
      for word in block:
        s = s + word + " "
      if len(block) <= 50:
        split[-1] += s
      else:
        split.append(s)  
    return split  

  def transcribe_audio(self) -> str:
    result = self.whisper.transcribe(self.audio_file)
    self.transcription = result["text"]
    return self.transcription

  def take_notes(self, max_tokens: int=1000) -> str:
    generation_args = { 
    "max_new_tokens": max_tokens, 
    "return_full_text": False, 
    "do_sample": False, 
    } 
    if len(self.transcription.split()) > 400:
      split = self.__split_prompt()
      response = ""
      for i, prompt in enumerate(split):
        """"""
        s = ""
        if i == 0:
          messages = [ 
            {"role": "system", "content": "You are a college student taking notes for a lecture in Markdown formatting. Be detailed in your notes to avoid later confusion."},
            {"role": "user", "content": prompt},
          ]  
          s = self.llm(messages, **generation_args)[0]['generated_text']
          response = response + s + "\n\n"
        else:
          messages = [ 
            {"role": "system", "content": f"You are a college student taking notes for a lecture in Markdown formatting. Be detailed in your notes to avoid later confusion. \
              You have already started taking notes, right now you have just finished writing: {s} please continue taking notes in this same file with the next part of the lecture, you do NOT need to re-write a title for these notes."},
            {"role": "user", "content": prompt},
          ]  
          s = self.llm(messages, **generation_args)[0]['generated_text']
          response = response + s + "\n\n"
    else:
      messages = [ 
        {"role": "system", "content": "You are a college student taking notes for a lecture in Markdown formatting. Be detailed in your notes to avoid later confusion."},
        {"role": "user", "content": self.transcription},
      ]  
      self.notes = self.llm(messages, **generation_args)[0]['generated_text']
      return self.notes
    self.notes = response
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
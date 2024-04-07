from openai import OpenAI
import os
from pathlib import Path
from dataclasses import dataclass
from audio_splitter import split_audio
import argparse

@dataclass
class Lecture:
  audio_file: str
  audio_size: float
  split_list: list
  
def transcribe_audio(lecture: Lecture) -> str:
  transcription = ""
  if lecture.split_list != []:
    for f in lecture.split_list:
      audio_file = open(f, "rb")
      transcription += client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text",
      ) + " "
  else:
    audio_file = open(lecture.audio_file, "rb")
    transcription += client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file,
      response_format="text",
    )
  return transcription

def take_notes(transcription: str) -> str:
  response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a college student taking notes for a lecture in Markdown formatting. Be detailed in your notes to avoid later confusion."},
    {"role": "user", "content": transcription},
  ])
  return response.choices[0].message.content

def main():
  # Handle commandline arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("--api-key", type=str, help="OpenAI API key.")
  parser.add_argument("--audio-file", type=str, help="Path to audio file to take notes on.")
  opt = parser.parse_args()

  global client 
  client = OpenAI(api_key=opt.api_key) # instance of OpenAI used by transcriber and notetaker

  audio_file = opt.audio_file
  audio_path = Path(audio_file)
  file_stem = audio_path.stem
  output_dir = f"{os.getcwd()}/{file_stem}"
  
  lecture = Lecture(audio_file, (os.stat(audio_path).st_size / (1024 * 1024)), [])

  if lecture.audio_size > 8:
    split_audio(lecture.audio_file, output_dir, 300000, "mp3", False)
    for file in os.listdir(output_dir):
      lecture.split_list.append(f"{output_dir}/{file}")
    lecture.split_list.sort(key = lambda x: int(str(Path(x).stem)))

  transcription = transcribe_audio(lecture)

  if not os.path.exists(f"{output_dir}/output"):
        os.makedirs(f"{output_dir}/output")

  with open(f"{output_dir}/output/{file_stem}-transcription.txt", "w") as out:
    out.write(transcription)

  notes = take_notes(transcription)

  with open(f"{output_dir}/output/{file_stem}-notes.md", "w") as out:
    out.write(notes)

  print("Output saved to ", output_dir)

if __name__ == "__main__":
  main()
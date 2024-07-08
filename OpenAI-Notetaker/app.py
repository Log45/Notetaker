from lecture import Lecture
from openai import OpenAI
import os
from pathlib import Path
from audio_splitter import split_audio
import argparse

def main():
    # Handle commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", type=str, help="OpenAI API key.")
    parser.add_argument("--audio-file", type=str, help="Path to audio file to take notes on.")
    opt = parser.parse_args()

    client = OpenAI(api_key=opt.api_key) # instance of OpenAI used by transcriber and notetaker
    lecture = Lecture(opt.audio_file, [], client) # instance of Lecture class

    file_stem = Path(lecture.audio_file).stem
    output_dir = f"{os.getcwd()}/{file_stem}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    split_list = []
    if lecture.audio_size > 8:
        split_audio(lecture.audio_file, output_dir, 300000, "mp3", False)
    for file in os.listdir(output_dir):
        split_list.append(f"{output_dir}/{file}")
    split_list.sort(key = lambda x: int(str(Path(x).stem)))
    lecture.set_split_list(split_list)

    transcription = lecture.transcribe_audio()

    if not os.path.exists(f"{output_dir}/output"):
        os.makedirs(f"{output_dir}/output")

    with open(f"{output_dir}/output/{file_stem}-transcription.txt", "w") as out:
        out.write(transcription)

    notes = lecture.take_notes()

    with open(f"{output_dir}/output/{file_stem}-notes.md", "w", encoding="utf-8") as out:
        out.write(notes)

    print("Output saved to ", output_dir)

if __name__ == "__main__":
  main()
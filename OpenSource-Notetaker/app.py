from lecture import Lecture
import os
from pathlib import Path
import argparse

def main():
    # Handle commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--whisper", type=str, help="Size of the whisper model to use. Options are tiny[.en], base[.en], small[.en], medium[.en], and large.")
    parser.add_argument("--audio-file", type=str, help="Path to audio file to take notes on.")
    opt = parser.parse_args()

    lecture = Lecture(opt.audio_file, [], opt.whisper) # instance of Lecture class

    file_stem = Path(lecture.audio_file).stem
    output_dir = f"{os.getcwd()}/{file_stem}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    transcription = lecture.transcribe_audio()

    if not os.path.exists(f"{output_dir}/output"):
        os.makedirs(f"{output_dir}/output")

    with open(f"{output_dir}/output/{file_stem}-transcription.txt", "w", encoding="utf-8") as out:
        out.write(transcription)

    notes = lecture.take_notes()

    with open(f"{output_dir}/output/{file_stem}-notes.md", "w", encoding="utf-8") as out:
        out.write(notes)

    print("Output saved to ", output_dir)

if __name__ == "__main__":
  main()
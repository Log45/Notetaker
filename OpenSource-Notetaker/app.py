from lecture import Lecture
import os
from pathlib import Path
import argparse
import whisper
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def main():
    # Handle commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--whisper", type=str, default="base.en", help="Size of the whisper model to use. Options are tiny[.en], base[.en], small[.en], medium[.en], and large.")
    parser.add_argument("--audio-file", type=str, help="Path to audio file to take notes on.")
    parser.add_argument("--model", type=str, default="microsoft/Phi-3-mini-128k-instruct", help="Model to use for lecture notes. Default is microsoft/Phi-3-mini-128k-instruct.")
    opt = parser.parse_args()

    client = whisper.load_model(opt.whisper)
    model = AutoModelForCausalLM.from_pretrained( 
    opt.model,  
    device_map="cuda",  
    torch_dtype="auto",  
    trust_remote_code=True,  
    ) 
    tokenizer = AutoTokenizer.from_pretrained(opt.model) 
    pipe = pipeline( 
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
    ) 

    lecture = Lecture(whisper_client=client, llm_pipeline=pipe, audio_file=opt.audio_file,) # instance of Lecture class

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
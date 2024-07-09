import whisper
import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model = whisper.load_model("medium.en")
result = model.transcribe("/home/log/Documents/Notetaker/jjk.mp3")
transcription = result["text"]

print(transcription)
print(len(transcription.split()))
 
torch.random.manual_seed(0) 
model = AutoModelForCausalLM.from_pretrained( 
    "microsoft/Phi-3-mini-128k-instruct",  
    device_map="cuda",  
    torch_dtype="auto",  
    trust_remote_code=True,  
) 

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct") 

pipe = pipeline( 
    "text-generation", 
    model=model, 
    tokenizer=tokenizer, 
) 

def __split_prompt() -> list:
    splt = transcription.split()
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

def take_notes(max_tokens: int=1000) -> str:
    """Implement this function to take notes from the lecture transcription using an open source model like Phi-3, ollama, or something else."""
    generation_args = { 
    "max_new_tokens": max_tokens, 
    "return_full_text": False, 
    "do_sample": False, 
    } 
    if len(transcription.split()) > 400:
      split = __split_prompt()
      response = ""
      for i, prompt in enumerate(split):
        """"""
        s = ""
        if i == 0:
          messages = [ 
            {"role": "system", "content": "You are a college student taking notes for a lecture in Markdown formatting. Be detailed in your notes to avoid later confusion."},
            {"role": "user", "content": prompt},
          ]  
          s = pipe(messages, **generation_args)[0]['generated_text']
          response = response + s + " (inference cutoff)\n"
        else:
          messages = [ 
            {"role": "system", "content": f"You are a college student taking notes for a lecture in Markdown formatting. Be detailed in your notes to avoid later confusion. \
              You have already started taking notes, right now you have just finished writing: {s} please continue taking notes in this same file with the next part of the lecture, you do not need to re-write a title for these notes."},
            {"role": "user", "content": prompt},
          ]  
          s = pipe(messages, **generation_args)[0]['generated_text']
          response = response + s + " (inference cutoff)\n"
    else:
      messages = [ 
        {"role": "system", "content": "You are a college student taking notes for a lecture in Markdown formatting. Be detailed in your notes to avoid later confusion."},
        {"role": "user", "content": transcription},
      ]  
      return pipe(messages, **generation_args)[0]['generated_text']
    return response

output = take_notes()
print(len(output.split()))

with open("jjk.md", "w", encoding="utf-8") as out:
    out.write(output)
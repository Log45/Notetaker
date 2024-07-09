import whisper
import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model = whisper.load_model("base.en")
result = model.transcribe("C:/Users/Logan/Documents/CODE/Notetaker/OpenSource-Notetaker/M3DemoAnonymization_Logan.mp3")
transcription = result["text"]

 

torch.random.manual_seed(0) 
model = AutoModelForCausalLM.from_pretrained( 
    "microsoft/Phi-3-mini-128k-instruct",  
    device_map="cuda",  
    torch_dtype="auto",  
    trust_remote_code=True,  
) 

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct") 

messages = [ 
    {"role": "system", "content": "You are a college student taking notes for a lecture in Markdown formatting. Be detailed in your notes to avoid later confusion."},
    {"role": "user", "content": transcription},
] 

pipe = pipeline( 
    "text-generation", 
    model=model, 
    tokenizer=tokenizer, 
) 

generation_args = { 
    "max_new_tokens": 500, 
    "return_full_text": False, 
    "temperature": 0.0, 
    "do_sample": False, 
} 

output = pipe(messages, **generation_args) 
print(output[0]['generated_text'])
import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
from datasets import load_dataset

print(torch.cuda.is_available())

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)


model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr").to(device)
processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")

print(model.device)

ds = load_dataset("hf-internal-testing/librispeech_asr_demo", "clean", split="validation", trust_remote_code=True)
print(f"File: {ds[0]['file']}")
print(ds)
print(ds[0]['audio'])
print(ds[0]['audio']['array'])

output = ""

for i in range(ds.num_rows):
  inputs = processor(ds[i]["audio"]["array"], sampling_rate=ds[i]["audio"]["sampling_rate"], return_tensors="pt").to(device)

  # print(ds[i]["audio"])

  generated_ids = model.generate(inputs["input_features"], attention_mask=inputs["attention_mask"])
  transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)
  output = output + transcription[0] + "\n"

with open("transcription.txt", "w") as out:
  out.write(output)

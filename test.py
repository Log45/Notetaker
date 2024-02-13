import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
import datasets
import soundfile as sf
from utils import *



filename = input("Enter audio filename: ")

# if(".mp3" in filename):
#   filename = mp3_to_flac(filename)
# elif(".flac" not in filename):
#   filename = misc_to_flac(filename)

data_dict = {"file": [filename]}
dataset = datasets.Dataset.from_dict(data_dict)
dataset = dataset.map(map_to_array, remove_columns=["file"])

print(dataset['audio'])

# dataset = SimpleDataset(data_files=filename)
# #print(dataset)

# dataset.download_and_prepare()

# dataset = dataset.as_dataset()

# dataset.map(map_to_array)

# print(dataset)

print(torch.cuda.is_available())

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)


model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr").to(device)
processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")

print(model.device)

input = processor(dataset['audio'], sampling_rate = 16000, return_tensors = "pt").to(device)
generated_ids = model.generate(input["input_features"], attention_mask=input["attention_mask"])
transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)

with open("memorial.txt", "w") as out:
    out.write(transcription[0])

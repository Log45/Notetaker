import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
import datasets
import soundfile as sf
from utils import *



filename = input("Enter audio filename: ")

if(".mp3" in filename):
  filename = mp3_to_flac(filename)
elif(".flac" not in filename):
  filename = misc_to_flac(filename)

data_dict = {"file": [filename]}
dataset = datasets.Dataset.from_dict(data_dict)
dataset = dataset.map(map_to_array, remove_columns=["file"])

# print(dataset['audio'])

# dataset = SimpleDataset(data_files=filename)
# #print(dataset)

# dataset.download_and_prepare()

# dataset = dataset.as_dataset()

# dataset.map(map_to_array)

# print(dataset)

print(torch.cuda.is_available())

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(device)


model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-large-librispeech-asr").to(device)
processor = Speech2TextProcessor.from_pretrained("facebook/s2t-large-librispeech-asr")

print(model.device)

#print(dataset['audio'][0][0])
#print(dataset['audio'])

dataset = torch.tensor(dataset['audio'])
print(f"dim: {dataset.dim()}")
print("Shape:", dataset.shape)

# with open("data.txt", "w") as out:
#     for t in dataset[0]:
#         out.write(t.__str__())

# dataset = torch.squeeze(dataset)
# print("New Shape: ", dataset.shape)

# dataset = torch.split(torch.flatten(dataset), 80)
# print("Split Shape: ", torch.stack(list(dataset)).shape)

dataset = torch.flatten(dataset)
print("Flatten Shape: ", dataset.shape)



input = processor(dataset, sampling_rate = 16000, return_tensors = "pt").to(device)

print(input)
print("Input Shape: ", input["input_features"].shape)

generated_ids = model.generate(input["input_features"], attention_mask=input["attention_mask"])
transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)

print(transcription)

with open("memorial.txt", "w") as out:
    out.write(transcription[0])

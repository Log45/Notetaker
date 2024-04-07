import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
from transformers import TrainingArguments, Trainer
from utils import *
from librispeech_handler import get_data
from datasets import *

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
# if device == "cpu":
#   device = "mps" if torch.backends.mps.is_available() else "cpu"
print(device)

training_args = TrainingArguments(output_dir="test_trainer", evaluation_strategy="epoch")
model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-large-librispeech-asr").to(device)
processor = Speech2TextProcessor.from_pretrained("facebook/s2t-large-librispeech-asr")

data_dict = get_data()
dataset_lst = []

for file in data_dict.keys():
  file_dict = {"file": [file],
               "text": [data_dict[file]]}
  #print(file_dict)
  file_ds = Dataset.from_dict(file_dict)
  dataset = file_ds.map(map_to_array, remove_columns=["file"])
  dataset_lst.append(dataset)

#print(dataset_lst)

dataset = interleave_datasets(dataset_lst)

#Dataset.train_test_split()

print(dataset)

datasets_dict = dataset.train_test_split(test_size=0.2)

print(datasets_dict)

model.train(True)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=datasets_dict["train"],
    eval_dataset=datasets_dict["test"],
    compute_metrics=compute_metrics,
)

if __name__ == "__main__":
  trainer.train()
  

import os
from os.path import *
from dataclasses import dataclass

# @dataclass
# class LibriSpeechData:
#   filename: str
#   text: str


def get_data():
  cwd = os.getcwd()
  #print(cwd)
  #print(os.listdir(cwd))
  if "LibriSpeech" in os.listdir(cwd):
    PATH = f"{cwd}/LibriSpeech"
    #print("LibriSpeech found!")
    dir_list = []
    #print(os.listdir("LibriSpeech"))
    for d in os.listdir("LibriSpeech"):
      if isdir(f"{PATH}/{d}"):
        #print(d)
        dir_list.append(f"{PATH}/{d}")
    #print(dir_list)
    data_dict = {}
    
    # Iterate through the dataset, readers, and chapters (to access the audio files and transcripts)
    for data in dir_list:
      #print(data)
      if data[0] == ".":
        pass
      for reader in os.listdir(data):
        #print(reader)
        if reader == ".DS_Store":
          pass
        for chapter in os.listdir(f"{data}/{reader}"):
          #print(chapter)
          if chapter[0] == ".":
            pass
          for file in os.listdir(f"{data}/{reader}/{chapter}"):
            if file[0] == ".":
              pass
            if(isfile(f"{data}/{reader}/{chapter}/{file}")):
              if ".txt" in file:
                with open(f"{data}/{reader}/{chapter}/{file}", "r") as f:
                  for line in f:
                    lst = line.split(" ", 1)
                    data_dict[f"{data}/{reader}/{chapter}/{lst[0]}.flac"] = lst[1]  
    return data_dict                      
  else:
    print("LibriSpeech not found...")
    return None

if __name__ == "__main__":
  d = get_data()
  print(d, len(d))
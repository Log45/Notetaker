# NoteTaker

This project is meant to eventually be a webapp, but the general idea is to take an .mp3 (or other audio format) file of a lecture or a meeting, generate a text transcript of that audio file, and create notes for that meeting or lecture.

## Status:
Currently I am messing around with an open-source Speech-to-Text model from facebook. Ignore the spaghetti code currently there. 

## Issues:
I need to figure out how to:
1. Split a single audio file into workable batches
2. Ensure those batches have a dimension of 1

## Todo:
1. Fix issues (see above)
2. Create a pipeline for taking the transcription and creating (hopefully formatted) notes
3. Turn it into a webapp (Flask)

### Datasets to Train On
- TED-LIUM (https://www.openslr.org/51)
- LibriSpeech ASR (https://openslr.org/12)
- Audio-MNIST (https://github.com/soerenab/AudioMNIST)

## Instructions
- Create a virtual environment with Python 3.8 and then enter the following commands:
```shell
brew install ffmpeg # or use apt for linux
pip3 install requirements.txt
```

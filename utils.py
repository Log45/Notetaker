import datasets
from datasets import Split, ReadInstruction, DatasetInfo, Features
from datasets.data_files import DataFilesDict
import soundfile as sf
from os import path
from pydub import AudioSegment


def map_to_array(batch):
    speech_array, _ = sf.read(batch["file"])
    batch["audio"] = speech_array
    return batch

def mp3_to_flac(audio_file: str):
    """"""
    dst = audio_file[:-3] + "flac"
    print(dst)

    sound = AudioSegment.from_mp3(audio_file)
    sound.export(dst, format="flac")
    return dst

def misc_to_flac(audio_file: str):
    lst = audio_file.split(".")
    dst = ""
    for i in range(lst-1):
        dst = dst+lst[i]
    dst = dst+".flac"
    sound = AudioSegment.from_file(audio_file)
    sound.export(dst, format="flac")
    return dst

# class SimpleConfig(datasets.BuilderConfig):
#     """BuilderConfig for SimpleDataset."""

#     def __init__(self, **kwargs):
#         """
#         Args:
#           data_dir: `string`, the path to the folder containing the files in the
#             downloaded .tar
#           citation: `string`, citation for the data set
#           url: `string`, url for information about the data set
#           **kwargs: keyword arguments forwarded to super.
#         """
#         super(SimpleConfig, self).__init__(version=datasets.Version("2.1.0", ""), **kwargs)

# class SimpleDataset(datasets.DatasetBuilder):
#     """ Simple Dataset """
#     BUILDER_CONFIGS = [
#         SimpleConfig(name="clean", description="'Clean' speech."),
#         SimpleConfig(name="other", description="'Other', more challenging, speech."),
#     ]

#     def __init__(self, cache_dir = None, dataset_name = None, config_name= None, hash= None, base_path= None, info= None, features= None, token=None, use_auth_token="deprecated", repo_id= None, data_files= None, data_dir= None, storage_options= None, writer_batch_size= None, name="deprecated", **config_kwargs):
#         super().__init__(cache_dir, dataset_name, config_name, hash, base_path, info, features, token, use_auth_token, repo_id, data_files, data_dir, storage_options, writer_batch_size, name, **config_kwargs)

#     def _download_and_prepare(self, dl_manager=None, verification_mode=None, **prepare_split_kwargs):
#         return #super()._download_and_prepare(dl_manager, verification_mode, **prepare_split_kwargs)

#     def _info(self):
#         return datasets.DatasetInfo(
#             description="Just a dataset to hold one audio file.",
#             features=datasets.Features(
#                 {
#                     "file": datasets.Value("string"),
#                     "audio": datasets.features.Audio(sampling_rate=16_000),
#                 }
#             )
#           )
#     def _as_dataset(self, split= Split.ALL, in_memory: bool = False) -> datasets.Dataset:
#         return super()._as_dataset(split, in_memory)
    

import os
import shutil
from pathlib import Path


def mkdir(dir_path: str):
    sub_dir = Path(dir_path)
    if not sub_dir.exists():
        sub_dir.mkdir(parents=True)


def scan_dir(dir_path: str):
    folders = {}
    for entry in os.scandir(dir_path):
        if entry.is_dir():
            folders[entry.name] = entry

    return folders


def scan_files(dir_path: str, exts='*.*'):
    files = []
    for data_path in Path(dir_path).glob(exts):
            files.append(data_path)

    files.sort(reverse=False)
    # for data_path in Path(dir_path).glob(exts):
    #     if '.*' not in exts:
    #         if data_path.suffix.lower() not in exts:
    #             continue
    #     elif data_path.is_dir():
    #         continue
    #
    #     files.append(data_path)

    return files


def clean_up(dir_path: str):
    shutil.rmtree(dir_path, ignore_errors=True)

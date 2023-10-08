"""
Utils for accessing server cookie's folder, performing CRUD on the parquet files 
"""
from typing import Literal, Optional
from os import listdir, scandir


def split_parquet(s):
    return s.split('.parquet.gzip')[0]


def get_uploads(hashed_dir: str, return_type: Literal["parquet", "strip"] = 'parquet'):
    """
    Get the files of the folder `hashed_dir`

    """
    file_path = f'uploads/{hashed_dir}'
    if return_type == "parquet":
        return listdir(file_path)
    else:
        return [split_parquet(i) for i in listdir(file_path)]

def get_dir_size(path='.'):
    total = 0
    with scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total
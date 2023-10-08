"""
Contain services (or functions) to work with upload-related logic
"""
from io import BytesIO
from os import path, mkdir, remove
from pathlib import Path
from fastapi import UploadFile
from pandas import read_csv, read_excel
from db import Client
from errors import *
from services.folder import get_uploads, get_dir_size


def ensure_upload_path(path_name):
    destination = f'uploads/{path_name}'
    if not path.exists(destination):
        mkdir(destination)



def validate_upload_files(files: list[UploadFile], client: Client) -> list[UploadFile]:
    """
    Validate upload files, return the files or raise Exceptions

    @ Exceptions subclass:
    - DuplicateUploadFile
    - ClientMaxUssage
    - FileExceedUssage
    - FileExtensionInvalid

    """
    # check duplicated files (on request)
    file_set = {Path(i.filename).stem for i in files}
    if len(file_set) != len(files):
        raise DuplicateUploadFile

    # check existed files (on file system)
    if len(file_set.intersection({*get_uploads(client.server_cookie, return_type='strip')})) > 0:
        raise UploadedFileExisted

    # check total file size
    total_size = sum([i.size for i in files])
    if total_size - get_dir_size(f'uploads/{client.server_cookie}') < 0:
        raise ClientMaxUssage

    # check single file size
    valid_size = all([i.size <= 1 * (10**8) for i in files])
    if valid_size is False:
        raise FileExceedUssage

    # Check file extension
    accepted_content_type = (
        'text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    valid_ext = all([i.content_type in accepted_content_type for i in files])
    if valid_ext is False:
        raise FileExtensionInvalid

    return files


def save_upload_file(file: UploadFile, hashed_dir: str):
    destination = f'uploads/{hashed_dir}'
    try:
        contents = file.file.read()
        file_data = BytesIO(contents)
        if file.content_type == 'text/csv':
            df = read_csv(file_data)
        else:
            df = read_excel(file_data)
        df.to_parquet(
            destination + f'/{Path(file.filename).stem}.parquet.gzip', compression='gzip')

    except Exception:
        if path.exists(destination + f'/{Path(file.filename).stem}.parquet.gzip'):
            remove(destination + f'/{Path(file.filename).stem}.parquet.gzip')
        raise ParquetConversionError

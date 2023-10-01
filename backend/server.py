from fastapi import FastAPI, UploadFile, HTTPException, Form, Header, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Annotated
from random import randint, seed
from os import mkdir, path, listdir, remove
import pandas as pd
from io import BytesIO
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from template import template
import cohere
import duckdb
import re
from uuid import uuid4
from pathlib import Path
from typing import Optional
from db import ClientUtils, Client, engine
from errors import *
from sqlalchemy.orm import Session


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = 'vSULf5lQOyNZ9mUaOFjIuMlwmYkbafZikmXtH8c1'
co = cohere.Client(API_KEY)
env = Environment(loader=FileSystemLoader('templates'))


# db = {}
aliases = {}


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def get_client_id(request: Request):
    client_header = request.headers.get('client-id')
    if client_header is None:
        raise HeaderMissing
    return client_header


def split_parquet(s):
    return s.split('.parquet.gzip')[0]


def UploadAuthenticationFlow(request: Request, session: Session) -> Client:
    try:
        client_utils = ClientUtils(session)
        client_header = get_client_id(request)
        client_in_db = client_utils.find_client(client_header)
        client_utils.verify_client(client_in_db)
        return client_in_db

    except (HeaderMissing, ClientNotFound) as e:
        new_client_id = str(uuid4())
        new_client = client_utils.create_client(new_client_id)
        return new_client

    except ClientTimeOut as e:
        new_client_id = str(uuid4())
        client_utils.update_refresh_token(client_in_db, new_client_id)
        return client_in_db


def QuestionAuthenticationFlow(client_id: str, session: Session) -> Client:
    try:
        client_utils = ClientUtils(session)
        client_in_db = client_utils.find_client(client_id)
        client_utils.verify_client(client_in_db)
        return client_in_db

    except (ClientNotFound, ClientTimeOut) as e:
        raise TokenUnAuth



def UploadCheckingFlow(files: list[UploadFile], client: Client) -> list[UploadFile]:
    """
    Validate upload files, return the files or raise Exceptions

    @ Exceptions subclass:
    - DuplicateUploadFile
    - ClientMaxUssage
    - FileExceedUssage
    - FileExtensionInvalid

    """
    # check duplicated files (on upload)
    file_set = {Path(i.filename).stem for i in files}
    if len(file_set) != len(files):
        raise DuplicateUploadFile

    # check existed files (no-overwrite)
    files_in_dir = listdir(f'./uploads/{client.server_cookie}')

    if len(file_set.intersection({split_parquet(f) for f in files_in_dir})) > 0:
        raise UploadedFileExisted

    # check total file size
    total_size = sum([i.size for i in files])
    if total_size - client.total_consume < 0:
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


def create_hash_str(s):
    seed(1)
    hashed = str(randint(1_000_000, 9_999_999_999))
    return s + '_' + hashed


def ensure_upload_path(path_name):
    destination = f'uploads/{path_name}'
    if not path.exists(destination):
        mkdir(destination)


def save_upload_file(file: UploadFile, hashed_dir: str):
    destination = f'uploads/{hashed_dir}'
    if not path.exists(destination):
        mkdir(destination)

    contents = file.file.read()
    file_data = BytesIO(contents)
    if file.content_type == 'text/csv':
        df = pd.read_csv(file_data)
    else:
        df = pd.read_excel(file_data)

    try:
        df.to_parquet(
            destination + f'/{Path(file.filename).stem}.parquet.gzip', compression='gzip')
    except Exception as e:
        if path.exists(destination + f'/{Path(file.filename).stem}.parquet.gzip'):
            remove(destination + f'/{Path(file.filename).stem}.parquet.gzip')
        raise ParquetConversionError


def analyze_df(df):
    col_type = df.dtypes.to_dict()
    null_counts = df.isnull().sum().to_dict()

    a = {}
    for index in col_type.keys():
        a[index] = (str(col_type[index]), null_counts[index])
    return a


@app.get("/")
async def root():
    return {"response": "Hello World"}


@app.post('/test_pandas_reading')
async def test_pandas_reading(files: list[UploadFile]):
    dfs = []
    try:
        for file in files:
            contents = file.file.read()
            file_data = BytesIO(contents)
            if file.content_type == 'text/csv':
                df = pd.read_csv(file_data)
            else:
                df = pd.read_excel(file_data)

            dfs.append({'name': file.filename, 'info': analyze_df(df)})
        return dfs
    except Exception as e:
        raise HTTPException(400, {'origin': file.filename, 'error': str(e)})


@app.post("/uploadfiles")
async def create_upload_files(files: list[UploadFile], request: Request, session: Session = Depends(get_session)):
    client = UploadAuthenticationFlow(request, session)

    ensure_upload_path(client.server_cookie)

    try:
        valid_files = UploadCheckingFlow(files, client)
        for f in valid_files:
            save_upload_file(f, client.server_cookie)
        response = JSONResponse(content='File upload successfully')
        response.set_cookie(key="client-id", value=client.client_cookie)
        return response

    except (DuplicateUploadFile, UploadedFileExisted):
        raise HTTPException(400, 'Duplicate uploaded file name')
    except ClientMaxUssage:
        raise HTTPException(400, 'Exceed 500MB of total upload files')
    except FileExceedUssage:
        raise HTTPException(400, 'Uploaded file exceed 100MB')
    except FileExtensionInvalid:
        raise HTTPException(400, 'File extension not .csv or .xlsx')
    except ParquetConversionError:
        raise HTTPException(
            400, 'Cannot convert file to parquet. Make sure columns having the same type or pandas readable')


def get_table_meta(file_path):
    df = duckdb.read_parquet(file_path)
    return [(i[0], i[1]) for i in df.description]


# @app.post('/ask-question')
@app.post('/ask-question')
async def ask_question(client_id: Annotated[str, Header()], question: Annotated[str, Form()],
                       table_name: Annotated[str, Form()], ai_explain: Optional[bool] = None,
                       session: Session = Depends(get_session)):

    try:
        client = QuestionAuthenticationFlow(client_id, session)

        upload_folder = f'uploads/{client.server_cookie}/{table_name}.parquet.gzip'

        return
    except TokenUnAuth:
        pass
    # alias = 'tbl_1'

    # prompt_tmpl = env.from_string(template)
    # schema = get_table_meta(file_name)
    # prompt = prompt_tmpl.render(
    #     table_alias=alias, schema=schema, question=question)

    # response = co.generate(prompt, model='command-nightly',
    #                        max_tokens=544, temperature=0)
    # sql_query = re.findall(r'```([^```]*)```', response.generations[0].text)[0]

    # if 'sql' in sql_query:
    #     sql_query = sql_query.split('\n')[1]

    # tbl = duckdb.read_parquet(file_name)
    # try:
    #     result = tbl.query(alias, sql_query)
    #     content = {"query": sql_query, "result": result.fetchall()}
    #     if ai_explain is not None and ai_explain:
    #         content['ai_explain'] = response.generations[0].text
    #     return content
    # except Exception:
    #     raise HTTPException(400, sql_query)

if __name__ == '__main__':
    uvicorn.run("__main__:app", reload=True)
